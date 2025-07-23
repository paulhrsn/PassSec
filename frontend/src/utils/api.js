const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5001/api";

  
//  @param {{ email: string, password: string }}
// @returns {Promise<{ token: string, user: object } | { error: string }>}
 
export async function loginUser({ email, password }) {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
    });

    const data = await res.json();

    if (!res.ok) {
      return { error: data.message || "Login failed" };
    }

    return { token: data.token, user: data.user };
  } catch (err) {
    console.error("loginUser network error:", err);
    return { error: "Network error" };
  }
}

 // @param {{ email: string, password: string }}
 // @returns {Promise<{ error: string }>}
 
 export async function registerUser({ email, password }) {
  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
    });

    const data = await res.json();

    if (!res.ok) {
      return { error: data.error || data.message || "Registration failed" };
    }

    return {}; //success
  } catch (err) {
    console.error("registerUser network error:", err);
    return { error: "Network error" };
  }
}




  
  //@param {{ domain?: string, count?: number }}
  //@returns {Promise<Array>} Array of quiz questions
 
export async function fetchQuizQuestions({ domain = "", count = 5 }) {
  const url = new URL(`${API_BASE}/quiz`);
  if (domain) url.searchParams.append("domain", domain);
  if (count)  url.searchParams.append("count", count);

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch quiz questions");

  return res.json();
}

  
  //@param {{ answers: Array<{ question_id: number, answer: string }> }}
  //@returns {Promise<{ score: number, total: number }>}
 
  export async function submitQuizAnswers({ answers, domain }) {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_BASE}/quiz/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` // ✅ add JWT here
      },
      body: JSON.stringify({ answers, domain })
    });
  
    if (!res.ok) throw new Error("Quiz submission failed");
    return res.json();
  }
  



 
 //@returns {Promise<Array>} List of lab summaries
 
export async function fetchAllLabs() {
  const res = await fetch(`${API_BASE}/labs`);
  if (!res.ok) throw new Error("Failed to fetch labs");
  return res.json();
}

 //@param {string|number} labId
 //@returns {Promise<object>} Lab data
 
export async function fetchLab(labId) {
  const res = await fetch(`${API_BASE}/labs/${labId}`);
  if (!res.ok) throw new Error(`Failed to fetch lab (${res.status})`);
  return res.json();
}

  
//  @param {{ userId: string, labId: string, answer: string }}
 // @returns {Promise<object>} Result (e.g. correct/incorrect)
 
export async function submitLabAnswer(data) {
  const res = await fetch(`${API_BASE}/labs/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Submission failed");
  return res.json();
}


export async function fetchUserStats() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_BASE}/dashboard/stats`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json(); // return an array of { domain, correct, total, percent }
}

 
 // @returns {Promise<{ status: string }>}
 
export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
