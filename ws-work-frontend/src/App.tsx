import { VehicleList } from './components/VehicleList';
import { VehicleForm } from './components/VehicleForm';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800 flex flex-col">
      <header className="bg-white shadow-sm py-4 sticky top-0 z-50">
        <div className="container mx-auto px-6 flex justify-between items-center">
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

      <main id="catalogo" className="flex-grow container mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 inline-block relative">
            Veículos Disponíveis
            <span className="absolute -bottom-2 left-0 w-full h-1 bg-ws-yellow"></span>
          </h2>
        </div>
        
        <VehicleList />
        
      </main>

      <section id="cadastro" className="bg-ws-gradient text-white py-16">
        <div className="container mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
          <div className="sticky top-24">
            <h2 className="text-4xl font-bold mb-4">Cadastre um novo veículo!</h2>
            <p className="text-gray-300 mb-8 leading-relaxed text-lg">
              Utilize nossa inteligência artificial para gerar descrições automáticas com base nos dados do seu veículo.
            </p>
          </div>

          <VehicleForm />
          
        </div>
      </section>
      
      <footer className="bg-ws-darkBlue text-gray-400 text-sm py-6 text-center border-t border-gray-800">
        <p>© WS Work Sistemas. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}