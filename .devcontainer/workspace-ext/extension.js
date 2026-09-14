// CSE 490 workspace: the screen a student sees on every open of the Project 5
// codespace, arranged by an extension because nothing in a config file can do it
// (editor tabs, sidebars and panel placement are workbench state).
//
// On activation, and on the command "CSE 490: Arrange the workspace":
//   1. close every editor tab
//   2. open ASSIGNMENT.md on the left, focused, and viewport.png (Blender's
//      live view) beside it, waiting for the container to write it
//   3. open Claude Code in the right-hand sidebar
//   4. focus a terminal below
const vscode = require("vscode");

const VIEW = "viewport.png";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function tryCommand(id, ...args) {
  try {
    await vscode.commands.executeCommand(id, ...args);
    return true;
  } catch (e) {
    return false;
  }
}

async function findView(maxWaitMs) {
  const folders = vscode.workspace.workspaceFolders || [];
  if (!folders.length) return null;
  const uri = vscode.Uri.joinPath(folders[0].uri, VIEW);
  const deadline = Date.now() + maxWaitMs;
  while (Date.now() < deadline) {
    try {
      await vscode.workspace.fs.stat(uri);
      return uri;
    } catch (e) {
      await sleep(2000);
    }
  }
  return null;
}

async function arrange(output) {
  output.appendLine(new Date().toISOString() + " arranging the workspace");
  await tryCommand("workbench.action.closeAllEditors");

  // Claude Code on the right. The extension may still be starting; a second
  // try after a pause covers it. Either command id is accepted by its versions.
  let claude = await tryCommand("claude-vscode.sidebar.open");
  if (!claude) {
    await sleep(3000);
    claude = await tryCommand("claude-vscode.sidebar.open") || await tryCommand("claude-vscode.window.open");
  }
  output.appendLine("claude code panel: " + (claude ? "opened" : "not available"));

  // The assignment on the left, focused: the answer to "where do I start".
  const folders = vscode.workspace.workspaceFolders || [];
  if (folders.length) {
    const asg = vscode.Uri.joinPath(folders[0].uri, "ASSIGNMENT.md");
    try {
      await vscode.workspace.fs.stat(asg);
      await vscode.commands.executeCommand("vscode.open", asg, { viewColumn: vscode.ViewColumn.One, preview: false });
      output.appendLine("assignment opened");
    } catch (e) {
      output.appendLine("no ASSIGNMENT.md in the workspace");
    }
  }

  // Blender's live view beside it, once the container has written it.
  const uri = await findView(90000);
  if (uri) {
    await vscode.commands.executeCommand("vscode.open", uri, { viewColumn: vscode.ViewColumn.Two, preview: false, preserveFocus: true });
    output.appendLine("live view opened");
  } else {
    output.appendLine("viewport.png not written yet; run the command again later");
  }

  // the explorer, not the extensions view, on the left
  await tryCommand("workbench.view.explorer");

  // The terminal below, for the student's harness.
  if (!vscode.window.terminals.length) {
    vscode.window.createTerminal({ name: "harness" });
  }
  await tryCommand("workbench.action.terminal.focus");
  output.appendLine("done");
}

let arranged = false;

function activate(context) {
  const output = vscode.window.createOutputChannel("CSE 490 workspace");
  context.subscriptions.push(output);
  context.subscriptions.push(
    vscode.commands.registerCommand("cse490.layout", () => arrange(output))
  );
  if (!arranged) {
    arranged = true;
    // let the workbench finish restoring its own state before rearranging it
    setTimeout(() => arrange(output).catch((e) => output.appendLine("error: " + e)), 2500);
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
