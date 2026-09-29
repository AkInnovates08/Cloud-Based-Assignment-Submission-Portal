# Security Design

- Passwords are hashed with bcrypt in local mode.
- JWTs are signed server-side and expire.
- Every protected endpoint validates authentication.
- Role checks prevent students from grading or accessing another student's files.
- File extension and file-size checks run server-side.
- File paths are generated from server-controlled IDs rather than trusting user paths.
- HTTPS should be mandatory in cloud deployment.
- Cloud storage buckets should remain private.
- Production downloads should use short-lived signed URLs.
- Database credentials and cloud service keys must remain in environment variables.
- CORS should contain only known frontend origins.
- Add rate limiting at the gateway/reverse proxy in production.
- Add malware scanning (for example, a quarantine bucket + scanning worker) before files become downloadable.
- Enable database/storage encryption at rest through the managed provider.
- Maintain audit logs for login, upload, grade, download, and authorization failures.
- Do not commit `.env`, service-role keys, passwords, database URLs, or private certificates.

Common mistakes:
1. Making assignment buckets public.
2. Trusting a role sent by the browser.
3. Trusting the client timestamp for deadlines.
4. Storing passwords in plain text.
5. Using original filenames as storage paths.
6. Allowing arbitrary extensions.
7. Returning another student's file URL.
8. Hardcoding cloud credentials.
