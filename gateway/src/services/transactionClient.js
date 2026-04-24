const baseUrl = process.env.TRANSACTION_SERVICE_URL || "http://localhost:8000";
const apiKey = process.env.TRANSACTION_SERVICE_API_KEY;

function buildHeaders() {
    return {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
    };
}

async function handleResponse(response) {
    const contentType = response.headers.get('Content-Type') || "";
    const body = contentType.includes('application/json')
        ? await response.json()
        : await response.text();

    if (!response.ok) {
        const error = new Error(`Transaction service error: ${response.status} ${response.statusText}`);
        error.status = response.status;
        error.details = body;
        throw error;
    }

    return body;
}

export async function createTransferRequest(transferData) {
    const response = await fetch(`${baseUrl}/api/transfers/`, {
        method: "POST",
        headers: buildHeaders(),
        body: JSON.stringify(transferData),
    });

    return handleResponse(response);
}

export async function fetchTransferById(transferId) {
    const response = await fetch(`${baseUrl}/api/transfers/${transferId}`, {
        method: "GET",
        headers: buildHeaders(),
    });

    return handleResponse(response);
}

export async function fetchTransfers(accountId) {
    const response = await fetch(`${baseUrl}/api/transfers/`, {
        method: "GET",
        headers: buildHeaders(),
    });

    return handleResponse(response);
}