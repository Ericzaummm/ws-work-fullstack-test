import type { Carro } from '../types';
import { VehicleCard } from './VehicleCard';

const mockCarros: Carro[] = [
  {
    id: 1,
    modelo_id: 101,
    nome_marca: 'Toyota',
    nome_modelo: 'Corolla XEI',
    ano: 2022,
    combustivel: 'Flex',
    num_portas: 4,
    cor: 'Branco',
    quilometragem: 35000,
    valor_anuncio: 125000,
    descricao: 'Veículo impecável, único dono, todas as revisões feitas na concessionária. Ótima oportunidade de negócio!',
  },
  {
    id: 2,
    modelo_id: 102,
    nome_marca: 'Honda',
    nome_modelo: 'Civic Touring',
    ano: 2021,
    combustivel: 'Gasolina',
    num_portas: 4,
    cor: 'Preto',
    quilometragem: 48000,
    valor_anuncio: 135000,
    descricao: 'Excelente estado de conservação. Motor turbo, teto solar e bancos em couro. Laudo cautelar 100% aprovado.',
  },
  {
    id: 3,
    modelo_id: 103,
    nome_marca: 'Volkswagen',
    nome_modelo: 'Nivus Highline',
    ano: 2023,
    combustivel: 'Flex',
    num_portas: 4,
    cor: 'Cinza',
    quilometragem: 15000,
    valor_anuncio: 130000,
    descricao: 'Carro de garagem, cheiro de novo. Pacote completo com painel digital e piloto automático adaptativo (ACC).',
  }
];

export function VehicleList() {
  return (
    
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {mockCarros.map((carro) => (
        <VehicleCard key={carro.id} carro={carro} />
      ))}
    </div>
  );
}