import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/">
          <h1 className="header-title">Party.Fight.Instigator</h1>
        </Link>
        <nav className="header-nav">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/game">Game</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;