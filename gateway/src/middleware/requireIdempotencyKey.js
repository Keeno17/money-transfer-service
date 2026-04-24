export function requireIdempotencyKey(req, res, next) {
    const idempotencyKey = req.get("Idempotency-Key");

    if (!idempotencyKey || !idempotencyKey.trim()) {
        return res.status(400).json({
            error: "Idempotency-Key header is required and cannot be empty",
        });
    }

    req.idempotencyKey = idempotencyKey.trim();
    next();
}