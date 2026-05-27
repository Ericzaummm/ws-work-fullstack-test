import { useState, useEffect } from 'react';
import type { Carro } from '../types';
import { VehicleCard } from './VehicleCard';
import { api } from '../services/api';

/**
 * Componente inteligente responsável por gerenciar 
 * o ciclo de vida da listagem de veículos.
 * * Ele lida de forma autônoma com a busca de dados na API (BFF) e aplica 
 * o padrão de Renderização Condicional para garantir a melhor UX possível.
 */
export function VehicleList() {
  // O uso do Generics <Carro[]> do TypeScript garante que o array só aceitará
  // objetos que cumpram o contrato estrito definido na nossa interface.
  const [carros, setCarros] = useState<Carro[]>([]);
  
  // Estados de controle de interface essenciais para uma boa experiência do usuário .
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * useEffect com array de dependências vazio [] atua como o antigo componentDidMount.
   * Ele executa a busca na API apenas uma vez, assim que o componente é montado na tela.
   */
  useEffect(() => {
    // Declaramos uma função assíncrona interna porque o callback do useEffect 
    // não pode ser async por padrão na arquitetura do React.
    async function fetchCarros() {
      try {
        const response = await api.get('/carros');
        setCarros(response.data);
        setError(null); // Limpa qualquer erro anterior caso a requisição tenha sucesso
      } catch (err) {
        console.error("Erro ao buscar veículos:", err);
        setError("Não foi possível carregar o catálogo de veículos no momento.");
      } finally {
        // O finally é executado independente do sucesso ou falha, 
        // garantindo que o spinner de carregamento seja desligado.
        setIsLoading(false);
      }
    }

    fetchCarros();
  }, []);

  // --- RENDERIZAÇÃO CONDICIONAL ---
  // A técnica de Early Return evita o aninhamento complexo de If/Else no JSX
  // e deixa a leitura do componente muito mais limpa e previsível.

  // 1. Estado de Carregamento 
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        {/* Animação de spinner nativa usando as utilidades do Tailwind */}
        <div className="w-12 h-12 border-4 border-ws-yellow border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium">Buscando veículos no banco de dados...</p>
      </div>
    );
  }

  // 2. Estado de Erro 
  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-center">
        <p className="text-red-600 font-semibold">{error}</p>
        {/* Oferece uma via de escape para o usuário tentar novamente */}
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  // 3. Estado Vazio
  if (carros.length === 0) {
    return (
      <div className="p-12 border-2 border-dashed border-gray-300 rounded-xl text-center bg-white">
        <p className="text-gray-500 text-lg">Nenhum veículo disponível no momento.</p>
      </div>
    );
  }

  // --- RENDERIZAÇÃO PRINCIPAL ---
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {/* A propriedade 'key' é obrigatória no React ao mapear arrays. 
        Ela otimiza a reconciliação do DOM, permitindo que o React atualize 
        apenas os cards que sofreram mutação.
      */}
      {carros.map((carro) => (
        <VehicleCard key={carro.id} carro={carro} />
      ))}
    </div>
  );
}