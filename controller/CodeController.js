import { spawn } from "child_process";

export const codeRunner = async (req, res) => {
  const { code, funcName, arg } = req.body;

  if (!code || !funcName || arg === undefined) {
    return res.status(400).json({ error: "Missing code, funcName or arg." });
  }

  try {
    const py = spawn("python3", ["simulate.py"]);

    let output = "";
    let error = "";

    py.stdout.on("data", (data) => {
      output += data.toString();
    });

    py.stderr.on("data", (data) => {
      error += data.toString();
    });

    py.on("close", () => {
      if (error) {
        console.error("Python error:", error);
        return res.status(500).json({ error: "Python script error", details: error });
      }

      try {
        const result = JSON.parse(output);
        res.json(result);
      } catch (err) {
        console.error("Invalid JSON:", output);
        res.status(500).json({ error: "Invalid response from Python" });
      }
    });

    // Send data as JSON string to simulate.py
    py.stdin.write(JSON.stringify({ code, funcName, arg }));
    py.stdin.end();
  } catch (err) {
    console.error("Server error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};
