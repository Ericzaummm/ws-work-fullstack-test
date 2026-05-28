/**
 * @fileoverview Contratos de Dados (Interfaces) da aplicação.
 * Estas interfaces garantem a tipagem estrita do TypeScript em todo o Front-end,
 * refletindo exatamente o schema (Pydantic/SQLAlchemy) definido no Back-end.
 */

/**
 * Representa a entidade Marca do veículo.
 */
export interface Marca {
  id: number;
  nome_marca: string;
}

/**
 * Representa o Modelo do veículo, mantendo a integridade relacional com a Marca.
 */
export interface Modelo {
  id: number;
  marca_id: number; // Chave estrangeira para a tabela de Marcas
  nome: string;
  valor_fipe: number;
}

/**
 * Entidade principal do sistema.
 * Contém os dados brutos do veículo e propriedades dinâmicas injetadas pelo BFF.
 */
export interface Carro {
  id: number;
  modelo_id: number;
  ano: number;
  combustivel: string;
  num_portas: number;
  cor: string;
  quilometragem: number;
  valor_anuncio: number;
  descricao: string;
  
  // Propriedades Opcionais 
  // O timestamp é gerado automaticamente pelo banco de dados no momento da inserção.
  timestamp_cadastro?: string;
  
  // --- DATA FLATTENING (BFF) ---
  // Decisão Arquitetural: Para evitar que o React precise fazer 3 requisições diferentes
  // (Carros, Modelos e Marcas) e cruzar os dados no Front-end, o nosso Back-end Python
  // atua como um BFF (Backend For Frontend), injetando os nomes já resolvidos diretamente
  // no objeto do carro na hora de devolver o JSON.
  nome_modelo?: string;
  nome_marca?: string;
}