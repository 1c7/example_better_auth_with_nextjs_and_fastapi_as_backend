import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.CONNECTION_STRING,
    }),
    emailAndPassword: {  
        enabled: true
    },
})