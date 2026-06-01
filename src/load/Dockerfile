FROM node:22-alpine AS build

WORKDIR /app

COPY src/load/package*.json ./
RUN npm install

COPY src/load/ ./

ARG VITE_URL_EP
ENV VITE_URL_EP=$VITE_URL_EP

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
