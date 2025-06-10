import { spawnSync } from "child_process";
import path from "path";

export const codeRunner = async (req, res) => {
  const code= JSON.parse(req.body.code);

  if (!code) {
    return res.status(400).json({ error: "No code provided" });
  }

  const pythonScriptPath = "simulate.py";

  try {
    const result = spawnSync("python", [pythonScriptPath], {
      input: code,
      encoding: "utf-8",
    });

    if (result.error) {
      return res.status(500).json({ error: "Python execution error", details: result.error });
    }

    const output = result.stdout.trim();
    const errorOutput = result.stderr.trim();

    if (errorOutput) {
      return res.status(500).json({ error: "Python stderr", details: errorOutput });
    }

    const parsed = JSON.parse(output);
    if (parsed.error) {
      return res.status(400).json({ error: parsed.error });
    }

    return res.json(parsed);
  } catch (err) {
    return res.status(500).json({ error: "Unexpected server error", details: err.message });
  }
};
