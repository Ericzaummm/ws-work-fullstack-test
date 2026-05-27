import type { Carro } from '../types';

/**
 * Interface que define as propriedades esperadas pelo componente VehicleCard.
 * @property {Carro} carro - Objeto tipado contendo todos os dados do veículo vindos da API.
 */
interface VehicleCardProps {
  carro: Carro;
}

/**
 * Componente de apresentação responsável por exibir 
 * os detalhes individuais de um veículo em formato de card.
 * * @param {VehicleCardProps} props - Propriedades do componente.
 * @returns {JSX.Element} Card renderizado com as informações do veículo.
 */
export function VehicleCard({ carro }: VehicleCardProps) {

  // Utiliza a API nativa Intl do JavaScript para formatação de moeda.
  // Decisão técnica: Evita a importação de bibliotecas externas pesadas e garante 
  // precisão com suporte automático à localização (pt-BR).
  const valorFormatado = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(carro.valor_anuncio);

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-100 hover:shadow-lg transition-shadow duration-300 flex flex-col h-full">
      
      {/* CABEÇALHO: Destaca o Modelo, Marca e Ano com as cores da identidade visual da WS Work */}
      <div className="bg-ws-darkBlue p-4 text-white">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="font-bold text-xl">{carro.nome_modelo || 'Modelo Indisponível'}</h3>
            <p className="text-ws-yellow text-sm font-semibold">{carro.nome_marca || 'Marca Indisponível'}</p>
          </div>
          <span className="bg-ws-yellow text-ws-darkBlue text-xs font-black px-2 py-1 rounded-sm">
            {carro.ano}
          </span>
        </div>
      </div>

      {/* CORPO DO CARD: Grid de especificações técnicas do veículo */}
      <div className="p-5 flex-grow flex flex-col gap-4 text-gray-700 text-sm">
        
        <div className="grid grid-cols-2 gap-y-3">
          <div className="flex flex-col">
            <span className="text-gray-400 text-xs font-semibold uppercase">Combustível</span>
            <span className="font-medium">{carro.combustivel}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-gray-400 text-xs font-semibold uppercase">Cor</span>
            <span className="font-medium">{carro.cor}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-gray-400 text-xs font-semibold uppercase">Portas</span>
            <span className="font-medium">{carro.num_portas}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-gray-400 text-xs font-semibold uppercase">KM</span>
            {/* toLocaleString adiciona automaticamente o separador de milhar (ex: 50.000) */}
            <span className="font-medium">{carro.quilometragem.toLocaleString('pt-BR')} km</span>
          </div>
        </div>

        {/* Linha divisória */}
        <div className="h-px w-full bg-gray-100 my-1"></div>

        {/* DESCRIÇÃO: Utiliza 'line-clamp-3' do Tailwind para truncar o texto após 3 linhas.
            Isso garante que descrições longas geradas pela IA não quebrem o alinhamento dos cards. */}
        <p className="text-gray-500 italic line-clamp-3">
          "{carro.descricao || 'Sem descrição cadastrada.'}"
        </p>

      </div>

      {/* RODAPÉ: Preço em destaque e Call to Action alinhado sempre na base do card (mt-auto) */}
      <div className="p-5 bg-gray-50 border-t border-gray-100 mt-auto">
        <div className="text-2xl font-black text-ws-darkBlue mb-3">
          {valorFormatado}
        </div>
        <button className="w-full bg-transparent border-2 border-ws-darkBlue text-ws-darkBlue font-bold py-2 rounded hover:bg-ws-darkBlue hover:text-white transition-colors">
          VER DETALHES
        </button>
      </div>
      
    </div>
  );
}