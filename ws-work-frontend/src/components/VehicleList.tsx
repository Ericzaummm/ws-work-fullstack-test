import { useState, useEffect } from 'react';
import type { Carro } from '../types';
import { VehicleCard } from './VehicleCard';
import { api } from '../services/api';

export function VehicleList() {
  const [carros, setCarros] = useState<Carro[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Busca os dados da api python
    async function fetchCarros() {
      try {
        const response = await api.get('/carros');
        setCarros(response.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar veículos:", err);
        setError("Não foi possível carregar o catálogo de veículos no momento.");
      } finally {
        setIsLoading(false);
      }
    }

    fetchCarros();
  }, []);

  // Renderização de estados especiais
  
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-12 h-12 border-4 border-ws-yellow border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium">Buscando veículos no banco de dados...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-center">
        <p className="text-red-600 font-semibold">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  if (carros.length === 0) {
    return (
      <div className="p-12 border-2 border-dashed border-gray-300 rounded-xl text-center bg-white">
        <p className="text-gray-500 text-lg">Nenhum veículo disponível no momento.</p>
      </div>
    );
  }

  // Renderização principal

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {carros.map((carro) => (
        <VehicleCard key={carro.id} carro={carro} />
      ))}
    </div>
  );
}