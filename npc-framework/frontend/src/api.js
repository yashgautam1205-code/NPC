const API_URL = "http://localhost:5000";

export async function sendMessage(npc_id, player_text) {
  let res;
  try {
    res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ npc_id, player_text }),
    });
  } catch {
    throw new Error("Cannot reach the chat backend. Check that it is running on port 5000.");
  }

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`The backend returned an invalid response (HTTP ${res.status}). Check its terminal for errors.`);
  }

  if (!res.ok) {
    throw new Error(data.error || `The chat request failed (HTTP ${res.status}).`);
  }

  return data;
}

export async function getMemories(npc_id) {
  const res = await fetch(`${API_URL}/memories`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ npc_id }),
  });
  return res.json();
}

export async function getAllMemories() {
  const res = await fetch(`${API_URL}/all-memories`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  return res.json();
}

export async function clearMemory(npc_id) {
  const res = await fetch(`${API_URL}/clear-memory`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ npc_id }),
  });
  return res.json();
}

export async function clearAllMemories() {
  const res = await fetch(`${API_URL}/clear-all-memories`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ confirm: true }),
  });
  return res.json();
}
