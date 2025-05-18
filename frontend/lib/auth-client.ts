import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: "http://localhost:8080"// 8080 运行着 nginx, 根地址 `/` 会 direct 给在 port 9000 运行的 next.js(本应用)
})

export const {
  signIn,
  signOut,
  signUp,
  useSession
} = authClient;