import GameLayout from '../components/GameLayout';

function Game() {
  return (
    <div className="game-page">
        <GameLayout>
          <h2 className="page-title">Game Mode</h2>
          <p>This is the PartyFightInstigator game page. Battle awaits!</p>
        </GameLayout>
    </div>
  );
}

export default Game;