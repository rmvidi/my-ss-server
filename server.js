const express = require("express");
const app = express();

// Route: /hello
app.get("/hello", (req, res) => {
  res.json({
    message: "Hello from your Termux API!",
    time: new Date()
  });
});

// Start server
app.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
