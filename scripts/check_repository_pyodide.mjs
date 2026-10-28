/* Execute each notebook's unchanged code in a separate pinned Pyodide process.
 * Runtime assets/wheels are an explicit, ignored test prerequisite. This checks
 * real WASM Python and piplite, not JupyterLite's browser UI/service-worker mount.
 */
import {readFile, readdir} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";
import {spawnSync} from "node:child_process";

const script=fileURLToPath(import.meta.url), root=path.resolve(path.dirname(script),"..");
const arg=name=>{const index=process.argv.indexOf(name);return index<0?null:process.argv[index+1];};
const runtimeDir=path.resolve(arg("--runtime") || path.join(root,"_build/pyodide-table-test"));
const lessonDir=path.join(root,"content/repository_examples"), notebookName=arg("--notebook");
if(!notebookName){
  const names=(await readdir(lessonDir)).filter(name=>/^\d\d_.*\.ipynb$/.test(name)).sort();
  if(names.length!==9)throw new Error("Expected nine notebooks");
  for(const name of names){
    const result=spawnSync(process.execPath,[script,"--runtime",runtimeDir,"--notebook",name],{stdio:"inherit"});
    if(result.status!==0)process.exit(result.status || 1);
  }
  console.log("All nine companions passed in fresh Pyodide processes.");
}else{
  const {loadPyodide}=await import(pathToFileURL(path.join(runtimeDir,"pyodide.mjs")));
  const runtime=await loadPyodide({indexURL:runtimeDir+path.sep});
  if(runtime.version!=="0.29.3")throw new Error(`Expected pinned Pyodide 0.29.3, found ${runtime.version}`);
  await runtime.loadPackage(["micropip","numpy","pandas","matplotlib","ipython"]);
  const extension=path.join(root,"dist/extensions/@jupyterlite/pyodide-kernel-extension/static/pypi");
  const piplite=(await readdir(extension)).find(name=>/^piplite-0\.7\.2-.*\.whl$/.test(name));
  if(!piplite)throw new Error("Build JupyterLite first to supply its actual piplite 0.7.2 wheel");
  runtime.FS.writeFile("/tmp/piplite.whl",await readFile(path.join(extension,piplite)));
  runtime.runPython(`
import zipfile, sysconfig
zipfile.ZipFile('/tmp/piplite.whl').extractall(sysconfig.get_path('purelib'))
import matplotlib
matplotlib.use('Agg')
`);
  runtime.FS.mkdirTree("/lessons");
  runtime.FS.mount(runtime.FS.filesystems.NODEFS,{root:lessonDir},"/lessons");
  runtime.FS.chdir("/lessons");
  const notebook=JSON.parse(await readFile(path.join(lessonDir,notebookName),"utf8"));
  let figureCount=0;
  runtime.runPython(`
import matplotlib.pyplot as plt, io
_verified_figures = 0
def _verify_show(*args, **kwargs):
    global _verified_figures
    for number in plt.get_fignums():
        buffer = io.BytesIO()
        plt.figure(number).savefig(buffer, format='png')
        assert len(buffer.getvalue()) > 1000
        _verified_figures += 1
    plt.close('all')
plt.show = _verify_show
`);
  for(let index=0;index<notebook.cells.length;index++){
    const cell=notebook.cells[index];
    if(cell.cell_type!=="code")continue;
    try{await runtime.runPythonAsync(cell.source.join(""));}
    catch(error){throw new Error(`${notebookName} cell ${index}: ${error.message}`);}
  }
  figureCount=runtime.runPython("_verified_figures");
  if(figureCount<3)throw new Error(`${notebookName}: fewer than three rendered figures`);
  console.log(JSON.stringify({notebook:notebookName,pyodide:runtime.version,piplite:runtime.runPython("__import__('piplite').__version__"),figures:figureCount,result:"pass"}));
}
