import Dial from '../components/Dial';
import DotPattern from '../components/DotPattern';
import VoiceDotCone from '../components/VoiceDotCone';

function Test() {
    return (
      <div>
        <Dial value={100} />    {/* Pointer at 54°, indicating 0 */}
        {/* <Dial value={50} />   Pointer at 284°, indicating 50
        <Dial value={100} />  Pointer at 154°, indicating 100 */}

        <hr />
        <h2>Dot Pattern Demo</h2>
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <p>Animation: Up</p>
            <DotPattern size={150} animationDirection="up" />
          </div>
          <div>
            <p>Animation: Down</p>
            <DotPattern size={150} animationDirection="down" />
          </div>
          <div>
            <p>Animation: None</p>
            <DotPattern size={150} animationDirection="none" />
          </div>
           <div>
            <p>Animation: Up (Small)</p>
            <DotPattern size={75} animationDirection="up" />
          </div>
        </div>
        <hr />
        <h2>Voice Dot Cone Demo</h2>
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <p>Animation: Up (Default Color)</p>
            <VoiceDotCone size={150} animationDirection="up" />
          </div>
          <div>
            <p>Animation: Down (Magenta)</p>
            <VoiceDotCone size={150} animationDirection="down" color="magenta" />
          </div>
          <div>
            <p>Animation: Up (Green)</p>
            <VoiceDotCone size={150} animationDirection="up" color="green" />
          </div>
          <div>
            <p>Animation: None</p>
            <VoiceDotCone size={150} animationDirection="none" color="red" />
          </div>
           <div>
            <p>Animation: Down (Small, Orange)</p>
            <VoiceDotCone size={75} animationDirection="down" color="orange" />
          </div>
        </div>
      </div>
    );
  }

export default Test;