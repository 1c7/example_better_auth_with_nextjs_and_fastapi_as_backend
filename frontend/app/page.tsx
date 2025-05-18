// import { createAuthClient } from "better-auth/react"
// const { useSession } = createAuthClient() 

// import Image from "next/image";
// import { authClient } from "@/lib/auth-client"
import { auth } from "@/auth"
import { headers } from "next/headers"

export default async function Home() {
  const session = await auth.api.getSession({
    headers: await headers()
  })
  console.log('session 是是是是', session);
  if (!session) {
    return (<div>
      Not logged in, visit <a href='/sign-up'>sign up</a> or <a href='/sign-in'>sign in</a>
    </div>)
  }
  const user = session.user
  // console.log('session', result);

  // const accounts = await authClient.listAccounts();
  // console.log('accounts', accounts);

  // 发请求给后端
  fetch('http://localhost:8080/backend')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });

  return (<div>Hi {user.email}, you are logged in!
    <br />
    <br />
    <a href='/logout'>Sign out</a>
  </div>);
}
