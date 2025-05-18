"use client"

import { signOut } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function LogoutPage() {
  const router = useRouter();
  
  signOut().then(() => {
    router.push("/");
  }).catch((error) => {
    console.error("Logout failed:", error);
    router.push("/");
  });
  
  return <div>登出中...</div>;
}
