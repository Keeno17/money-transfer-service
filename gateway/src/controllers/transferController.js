import {
    createTransferRequest,
    fetchTransferById,
    fetchTransfers,
} from "../services/transactionClient.js";

export async function createTransfer(req, res, next) {
    try {
        const payload = {
            ...req.body,
            idempotency_key: req.idempotencyKey,
        };

        const transfer = await createTransferRequest(payload);
        res.status(201).json(transfer);
    } catch (error) {
        next(error);
    }
}

export async function getTransferById(req, res, next) {
    try {
        const transfer = await fetchTransferById(req.params.id);
        res.status(200).json(transfer);
    } catch (error) {
        next(error);
    }
}

export async function listTransfers(req, res, next) {
    try {
        const transfers = await fetchTransfers();
        res.status(200).json(transfers);
    } catch (error) {
        next(error);
    }
}