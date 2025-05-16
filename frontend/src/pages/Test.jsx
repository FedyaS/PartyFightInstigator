import Dial from '../components/Dial';

function Test() {
    return (
      <div>
        <Dial value={100} />    {/* Pointer at 54°, indicating 0 */}
        {/* <Dial value={50} />   Pointer at 284°, indicating 50
        <Dial value={100} />  Pointer at 154°, indicating 100 */}
      </div>
    );
  }

export default Test;