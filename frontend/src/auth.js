export const decodeTokenPayload = (token) => {
  try {
    const payloadPart = token.split(".")[1];
    const payload = atob(payloadPart.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(payload);
  } catch {
    return null;
  }
};

export const getStoredAuth = () => {
  const token = localStorage.getItem("token");
  if (!token) {
    return { token: null, role: null, userId: null };
  }

  const payload = decodeTokenPayload(token);
  return {
    token,
    role: payload?.role ?? null,
    userId: payload?.user_id ?? null,
  };
};

export const clearAuth = () => {
  localStorage.removeItem("token");
};
