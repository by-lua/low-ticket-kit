# Coolify / any Docker host. Build: docker build -t checkout . — Run: docker run -p 4242:4242 --env-file .env -v checkout-data:/data checkout
# In Coolify: Build Pack = Dockerfile, port 4242, persistent storage mounted at /data, env vars from env.example (secrets only there).
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production PORT=4242 DATA_DIR=/data
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY catalog.mjs server.mjs ./
COPY src ./src
COPY public ./public
RUN mkdir -p /data && chown node:node /data
USER node
VOLUME ["/data"]
EXPOSE 4242
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||4242)+'/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "server.mjs"]
