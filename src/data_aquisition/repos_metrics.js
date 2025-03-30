import fs from "fs-extra";
import path from "path";
import { execSync } from "child_process";
import { createObjectCsvWriter } from "csv-writer";

const projectRoot = path.resolve(".");
const reposDir = path.join(projectRoot, "repos2");
const ckJarPath = path.join(projectRoot, "", "ck.jar");
const outputFile = path.join(projectRoot, "data", "metrics_results.csv");

if (!fs.existsSync(reposDir)) {
  console.error("Pasta 'repos' não encontrada!");
  process.exit(1);
}

fs.ensureDirSync(path.dirname(outputFile));

const csvWriter = createObjectCsvWriter({
  path: outputFile,
  header: [
    { id: "name", title: "Name" },
    { id: "loc", title: "LOC" },
    { id: "cbo_mean", title: "CBO Mean" },
    { id: "cbo_median", title: "CBO Median" },
    { id: "cbo_std", title: "CBO Std" },
    { id: "lcom_mean", title: "LCOM* Mean" },
    { id: "lcom_median", title: "LCOM* Median" },
    { id: "lcom_std", title: "LCOM* Std" }, // java -jar path/src/data_aquisition/ck.jar  /path/to/repo false 0 false /path/to/output 
    { id: "dit", title: "DIT" }
  ],
});

async function runCKAnalysis(repoPath, repoName) {
  try {
    console.log(`Analisando ${repoName}...`);
    const outputDir = path.join(repoPath, "ck_output");
    fs.ensureDirSync(outputDir);
    
    const cmd = `java -jar ${ckJarPath} ${repoPath} false 0 false ${outputDir}`;
    execSync(cmd, { stdio: "inherit" });

    const metricsFile = path.join(outputDir, "class.csv");
    if (!fs.existsSync(metricsFile)) return null;

    const data = fs.readFileSync(metricsFile, "utf-8").split("\n").slice(1);
    let loc = 0, cboValues = [], lcomValues = [], dit = 0;

    data.forEach(line => {
      const cols = line.split(",");
      if (cols.length < 4) return;
      
      const locVal = parseFloat(cols[3]);
      const cboVal = parseFloat(cols[1]);
      const lcomVal = parseFloat(cols[2]);
      const ditVal = parseFloat(cols[4]);

      if (!isNaN(locVal)) loc += locVal;
      if (!isNaN(cboVal)) cboValues.push(cboVal);
      if (!isNaN(lcomVal)) lcomValues.push(lcomVal);
      if (!isNaN(ditVal)) dit = Math.max(dit, ditVal);
    });

    return {
      name: repoName,
      loc,
      cbo_mean: cboValues.length ? (cboValues.reduce((a, b) => a + b, 0) / cboValues.length).toFixed(2) : 0,
      cbo_median: cboValues.length ? cboValues.sort((a, b) => a - b)[Math.floor(cboValues.length / 2)] : 0,
      cbo_std: cboValues.length ? Math.sqrt(cboValues.reduce((sq, n) => sq + Math.pow(n - (cboValues.reduce((a, b) => a + b, 0) / cboValues.length), 2), 0) / cboValues.length).toFixed(2) : 0,
      lcom_mean: lcomValues.length ? (lcomValues.reduce((a, b) => a + b, 0) / lcomValues.length).toFixed(2) : 0,
      lcom_median: lcomValues.length ? lcomValues.sort((a, b) => a - b)[Math.floor(lcomValues.length / 2)] : 0,
      lcom_std: lcomValues.length ? Math.sqrt(lcomValues.reduce((sq, n) => sq + Math.pow(n - (lcomValues.reduce((a, b) => a + b, 0) / lcomValues.length), 2), 0) / lcomValues.length).toFixed(2) : 0,
      dit,
    };
  } catch (error) {
    console.error(`Erro ao processar ${repoName}:`, error);
    return null;
  }
}

async function main() {
  const repoNames = fs.readdirSync(reposDir);
  const results = [];

  for (const repoName of repoNames) {
    const repoPath = path.join(reposDir, repoName);
    if (fs.lstatSync(repoPath).isDirectory()) {
      const result = await runCKAnalysis(repoPath, repoName);
      if (result) results.push(result);
    }
  }

  if (results.length) {
    await csvWriter.writeRecords(results);
    console.log("Métricas salvas em metrics_results.csv");
  } else {
    console.log("Nenhuma métrica coletada.");
  }
}

main().catch(console.error);
