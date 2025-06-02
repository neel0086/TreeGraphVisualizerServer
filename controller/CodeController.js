import { spawn } from "child_process";
export const codeRunner = async (req, res) => {
    const code = req.body.code;

    if (!code || typeof code !== "string") {
        return res.status(400).json({ error: "Missing or invalid code input." });
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

        py.on("close", (code) => {
            if (error) {
                console.error("Python error:", error);
                return res.status(500).json({ error: "Python script error", details: error });
            }

            try {
                const result = JSON.parse(output);
                res.json(result); // { nodes, edges, labels, root }
            } catch (err) {
                console.error("Invalid JSON:", output);
                res.status(500).json({ error: "Invalid response from Python" });
            }
        });

        // Send Python code to stdin of simulate.py
        py.stdin.write(code);
        py.stdin.end();
    } catch (err) {
        console.error("Server error:", err);
        res.status(500).json({ error: "Internal server error" });
    }
}

