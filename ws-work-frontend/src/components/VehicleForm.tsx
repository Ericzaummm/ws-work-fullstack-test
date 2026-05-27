import { useState } from 'react';
import { api } from '../services/api';

export function VehicleForm() {
  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    ano: '',
    cor: '',
    quilometragem: '',
    valor: '',
    descricao: ''
  });

  const [isLoadingAI, setIsLoadingAI] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const parseNumber = (val: string) => {
    if (!val) return 0;
    const cleanString = val.replace(/\./g, '').replace(',', '.');
    return Number(cleanString);
  };

  const handleGenerateDescription = async (e: React.MouseEvent) => {
    e.preventDefault();
    
    if (!formData.marca || !formData.modelo) {
      alert("Preencha ao menos a Marca e o Modelo para a IA gerar a descrição!");
      return;
    }

    setIsLoadingAI(true);
    
    try {
      const response = await api.post('/gerar-descricao', {
        marca: formData.marca,
        modelo: formData.modelo,
        ano: parseNumber(formData.ano),
        cor: formData.cor || 'Não informada',
        quilometragem: parseNumber(formData.quilometragem),
        valor: parseNumber(formData.valor)
      });

      setFormData(prev => ({
        ...prev,
        descricao: response.data.descricao
      }));
    } catch (error) {
      console.error("Erro ao gerar descrição com IA:", error);
      alert("Não foi possível gerar a descrição no momento.");
    } finally {
      setIsLoadingAI(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      marca_nome: formData.marca,
      modelo_nome: formData.modelo,
      ano: parseNumber(formData.ano),
      combustivel: "Flex", 
      num_portas: 4,       
      cor: formData.cor,
      quilometragem: parseNumber(formData.quilometragem),
      valor_anuncio: parseNumber(formData.valor),
      descricao: formData.descricao
    };

    try {
      await api.post('/carros', payload);
      alert("Veículo cadastrado com sucesso!");
      window.location.reload(); 
    } catch (error) {
      console.error('Erro ao salvar veículo:', error);
      alert("Ocorreu um erro ao salvar o veículo. Verifique o console.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-black/20 p-8 rounded-lg border border-ws-inputBorder shadow-xl">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        
        <div className="space-y-1 md:col-span-2">
          <label className="block text-sm font-medium text-gray-300">Marca / Modelo</label>
          <div className="flex gap-2">
            <input 
              required type="text" name="marca" placeholder="Ex: Honda"
              value={formData.marca} onChange={handleChange}
              className="w-1/3 h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
            />
            <input 
              required type="text" name="modelo" placeholder="Ex: Civic Touring"
              value={formData.modelo} onChange={handleChange}
              className="w-2/3 h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-300">Ano</label>
          <input 
            required type="text" inputMode="numeric" name="ano" placeholder="Ex: 2022"
            value={formData.ano} onChange={handleChange}
            className="w-full h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
          />
        </div>
        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-300">Cor</label>
          <input 
            required type="text" name="cor" placeholder="Ex: Preto"
            value={formData.cor} onChange={handleChange}
            className="w-full h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
          />
        </div>

        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-300">Quilometragem</label>
          <input 
            required type="text" inputMode="numeric" name="quilometragem" placeholder="Ex: 50.000"
            value={formData.quilometragem} onChange={handleChange}
            className="w-full h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
          />
        </div>
        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-300">Valor Anúncio (R$)</label>
          <input 
            required type="text" inputMode="numeric" name="valor" placeholder="Ex: 120.000,00"
            value={formData.valor} onChange={handleChange}
            className="w-full h-11 px-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors" 
          />
        </div>

        <div className="md:col-span-2 mt-2">
          <button 
            onClick={handleGenerateDescription}
            disabled={isLoadingAI}
            className="w-full py-3 bg-transparent border border-ws-yellow text-ws-yellow font-bold rounded-md hover:bg-ws-yellow hover:text-ws-darkBlue transition-all shadow-[0_0_15px_rgba(250,204,21,0.15)] disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
          >
            {isLoadingAI ? 'GERANDO...' : 'GERAR DESCRIÇÃO COM IA'}
          </button>
        </div>

        <div className="space-y-1 md:col-span-2 mt-2">
          <label className="block text-sm font-medium text-gray-300">Descrição do Anúncio</label>
          <textarea 
            required name="descricao" rows={4}
            value={formData.descricao} onChange={handleChange}
            placeholder="A descrição aparecerá aqui..."
            className="w-full p-4 bg-ws-inputBg border border-ws-inputBorder rounded-md text-white focus:outline-none focus:border-ws-yellow transition-colors resize-none" 
          ></textarea>
        </div>

      </div>

      <button type="submit" className="w-full mt-4 py-4 bg-white text-ws-darkBlue font-black text-lg rounded-md hover:bg-gray-100 transition-colors">
        SALVAR VEÍCULO
      </button>
    </form>
  );
}