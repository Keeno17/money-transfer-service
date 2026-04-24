import express from "express";

import transferRouter from "./routes/transferRoutes.js";
import { errorHandler } from "./middleware/errorHandler.js";
import { requestLogger } from "./middleware/requestLogger.js";

const app = express();

app.use(express.json());
app.use(requestLogger);

app.get("/health", (req, res) => {
    res.json({ status: "ok" })
});

app.use("/transfers", transferRouter);

app.use(errorHandler);

export default app;