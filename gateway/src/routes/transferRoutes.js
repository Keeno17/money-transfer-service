import express from 'express';
import {
    createTransfer,
    getTransferById,
    listTransfers,
} from '../controllers/transferController.js';
import { requireIdempotencyKey } from '../middleware/requireIdempotencyKey.js';

const router = express.Router();

router.post('/', requireIdempotencyKey, createTransfer);
router.get('/:id', getTransferById);
router.get('/', listTransfers);

export default router;