import fetch from "node-fetch";
import { execSync } from "child_process";
import fs from "fs-extra";
import { createObjectCsvWriter } from "csv-writer";
import dotenv from "dotenv";

dotenv.config();

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
if (!GITHUB_TOKEN) {
  throw new Error(" Erro: GITHUB_TOKEN não encontrado no .env!");
}

const GRAPHQL_QUERY = `
query($language: String!, $first: Int!, $after: String) {
  search(query: $language, type: REPOSITORY, first: $first, after: $after) {
    pageInfo { endCursor hasNextPage }
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazerCount
          createdAt
          url
          releases { totalCount }
          primaryLanguage { name }
        }
      }
    }
  }
}`;

async function fetchRepositories() {
  let repositories = [];
  let hasNextPage = true;
  let afterCursor = null;

  while (hasNextPage && repositories.length < 1000) {
    const response = await fetch("https://api.github.com/graphql", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${GITHUB_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: GRAPHQL_QUERY,
        variables: { language: "language:Java", first: 50, after: afterCursor },
      }),
    });

    const { data, errors } = await response.json();
    if (errors) {
      console.error(" Erro na API:", errors);
      return [];
    }

    const repos = data.search.edges.map((repo) => {
      const node = repo.node;
      return {
        name: node.nameWithOwner,
        stars: node.stargazerCount,
        age_in_years: ((new Date() - new Date(node.createdAt)) / (365 * 24 * 60 * 60 * 1000)).toFixed(2),
        releases: node.releases.totalCount,
        primary_language: node.primaryLanguage ? node.primaryLanguage.name : "N/A",
        url: node.url,
      };
    });

    repositories = [...repositories, ...repos];
    afterCursor = data.search.pageInfo.endCursor;
    hasNextPage = data.search.pageInfo.hasNextPage;

    console.log(` Coletados ${repositories.length} repositórios até agora...`);
  }

  return repositories;
}

function cloneRepository(repoUrl, repoName, baseDir = "repos") {
  const repoPath = `${baseDir}/${repoName.replace("/", "_")}`;
  if (!fs.existsSync(repoPath)) {
    console.log(` Clonando ${repoName}...`);
    execSync(`git clone ${repoUrl} ${repoPath}`, { stdio: "inherit" });
  } else {
    console.log(` Repositório ${repoName} já existe, pulando...`);
  }
  return repoPath;
}

function runCKAnalysis(repoPath) {
  const ckJarPath = "ck.jar"; 
  const outputDir = `${repoPath}/ck_output`;
  fs.ensureDirSync(outputDir);

  const cmd = `java -jar ${ckJarPath} ${repoPath} false 0 true ${outputDir}`;
  execSync(cmd, { stdio: "inherit" });

  const metricsFile = `${outputDir}/class.csv`;
  if (fs.existsSync(metricsFile)) {
    const data = fs.readFileSync(metricsFile, "utf-8").split("\n").slice(1);
    return data.map((line) => {
      const cols = line.split(",");
      return { class: cols[0], cbo: cols[1], dit: cols[2], lcom: cols[3] };
    });
  }

  return [];
}

async function saveToCSV(data, filename) {
  const csvWriter = createObjectCsvWriter({
    path: filename,
    header: Object.keys(data[0]).map((key) => ({ id: key, title: key })),
  });

  await csvWriter.writeRecords(data);
  console.log(` Dados salvos em ${filename}`);
}

async function main() {
  console.log(" Buscando repositórios...");
  const repos = await fetchRepositories();
  if (!repos.length) {
    console.error(" Nenhum repositório encontrado!");
    return;
  }

  await saveToCSV(repos, "repos_list.csv");

  const baseDir = "repos";
  fs.ensureDirSync(baseDir);

  let results = [];

  for (const repo of repos.slice(0, 1)) { 
    const repoPath = cloneRepository(repo.url, repo.name, baseDir);
    const metrics = runCKAnalysis(repoPath);

    for (const metric of metrics) {
      results.push({
        name: repo.name,
        stars: repo.stars,
        age_in_years: repo.age_in_years,
        releases: repo.releases,
        primary_language: repo.primary_language,
        url: repo.url,
        class: metric.class,
        cbo: metric.cbo,
        dit: metric.dit,
        lcom: metric.lcom,
      });
    }
  }

  if (results.length) {
    await saveToCSV(results, "metrics_results.csv");
  }
}


main().catch(console.error);
