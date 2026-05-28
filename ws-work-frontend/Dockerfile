# Usa a imagem oficial do Node.js
FROM node:20-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instala
COPY package*.json ./
RUN npm install

# Copia o resto do projeto React
COPY . .

# Expõe a porta padrão do Vite
EXPOSE 5173

# O --host 0.0.0.0 é crucial para que o Vite exponha a aplicação para fora do contêiner
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]