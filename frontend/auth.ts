import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.CONNECTION_STRING,
    }),
    emailAndPassword: {  
        enabled: true
    },
    plugins: [nextCookies()]
})