import { VehicleList } from './components/VehicleList';
import { VehicleForm } from './components/VehicleForm';

/**
 * Componente Raiz (Root Component) da aplicação.
 * Responsável por definir o Layout Global, a tipografia base e orquestrar 
 * a exibição dos componentes filhos (Smart e Dumb components).
 * * Decisões Arquiteturais de UI:
 * - HTML Semântico: Uso de <header>, <main>, <section> e <footer> para melhor SEO e Acessibilidade.
 * - Single Page Navigation: Navegação baseada em âncoras (#) para fluidez na mesma tela.
 */
export default function App() {
  return (
    // Wrapper principal: min-h-screen e flex-col garantem que o footer fique sempre 
    // no final da tela (Sticky Footer), mesmo se o conteúdo central for pequeno.
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800 flex flex-col">
      
      {/* CABEÇALHO / NAVEGAÇÃO 
          sticky top-0 z-50: Mantém o menu sempre visível no topo durante o scroll (Melhora a UX) */}
      <header className="bg-white shadow-sm py-4 sticky top-0 z-50">
        <div className="container mx-auto px-6 flex justify-between items-center">
          
          {/* Logo Componentizada visualmente */}
          <div className="flex items-center gap-2">
            <div className="bg-ws-yellow text-white font-black text-xl px-2 py-1 leading-none rounded-sm">
              WS<br/>work!
            </div>
            <span className="text-xl font-bold ml-2 text-ws-darkBlue border-l-2 border-gray-200 pl-4">
              Motors
            </span>
          </div>

          <nav>
            <ul className="flex space-x-8 text-sm font-semibold text-gray-600">
              <li><a href="#catalogo" className="hover:text-ws-yellow transition-colors">Catálogo</a></li>
              <li><a href="#cadastro" className="hover:text-ws-yellow transition-colors">Cadastrar Veículo</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* ÁREA PRINCIPAL: CATÁLOGO DE VEÍCULOS 
          flex-grow: Ocupa todo o espaço vertical disponível, empurrando o footer para baixo */}
      <main id="catalogo" className="flex-grow container mx-auto px-6 py-16">
        <div className="text-center mb-12">
          {/* Título com detalhe visual (pseudo-border) na cor da marca */}
          <h2 className="text-3xl font-bold text-gray-900 inline-block relative">
            Veículos Disponíveis
            <span className="absolute -bottom-2 left-0 w-full h-1 bg-ws-yellow"></span>
          </h2>
        </div>
        
        {/* Injeção do Container Component responsável por buscar e listar os carros */}
        <VehicleList />
        
      </main>

      {/* ÁREA SECUNDÁRIA: FORMULÁRIO DE CADASTRO E IA */}
      <section id="cadastro" className="bg-ws-gradient text-white py-16">
        {/* Grid responsivo: 1 coluna no celular (grid-cols-1), 2 colunas no desktop (md:grid-cols-2) */}
        <div className="container mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
          
          {/* Coluna da Esquerda (Textos de Chamada) 
              sticky top-24: Mantém o texto fixo na tela enquanto o usuário rola o formulário na direita */}
          <div className="sticky top-24">
            <h2 className="text-4xl font-bold mb-4">Cadastre um novo veículo!</h2>
            <p className="text-gray-300 mb-8 leading-relaxed text-lg">
              Utilize nossa inteligência artificial para gerar descrições automáticas com base nos dados do seu veículo.
            </p>
          </div>

          {/* Coluna da Direita: Injeção do formulário inteligente */}
          <VehicleForm />
          
        </div>
      </section>
      
      {/* RODAPÉ */}
      <footer className="bg-ws-darkBlue text-gray-400 text-sm py-6 text-center border-t border-gray-800">
        <p>© WS Work Sistemas. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}