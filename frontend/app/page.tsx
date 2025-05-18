import { auth } from "@/auth"
import { headers } from "next/headers"

export default async function Home() {
  const session = await auth.api.getSession({
    headers: await headers()
  })
  console.log('session 是', session);
  if (!session) {
    return (<div>
      Not logged in, visit <a href='/sign-up'>sign up</a> or <a href='/sign-in'>sign in</a>
    </div>)
  }
  const user = session.user
  console.log('user 是', user);

  // 发请求给后端
  fetch('http://localhost:8080/backend', {
    headers: {
      'Authorization': `Bearer ${session.session.token}`,
      'Content-Type': 'application/json'
    }
  }).then(response => {
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

  return (<div>Hi {user.email} ({user.name}), you are logged in!
    <br />
    <br />
    <a href='/logout'>Sign out</a>
  </div>);
}
