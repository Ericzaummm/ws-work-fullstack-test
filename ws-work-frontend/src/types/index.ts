export interface Marca {
  id: number;
  nome_marca: string;
}

export interface Modelo {
  id: number;
  marca_id: number;
  nome: string;
  valor_fipe: number;
}

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
  timestamp_cadastro?: string;
  
  nome_modelo?: string;
  nome_marca?: string;
}