import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Game from './pages/Game';
import Test from './pages/Test'
import Header from './components/Header';

function App() {
  return (
    <div style={{ margin: 0, padding: 0 }}> {/* Ensure no margins/padding */}
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game" element={<Game />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </div>
  );
}

export default App;