import {useEffect, useState} from "react";
import axios from "axios";
import './App.css';
import logo from './logo_reke.png';

function App() {
  const [intext, setIntext] = useState("")
  const [outsong, setOutsong] = useState("")
  const [issubmit, setIssubmit] = useState(false)

  useEffect(() => {
    axios
      .get("http://localhost:8080/initial")
      .catch((error) => alert(`Error: ${error.message}`))
  }, []);

  const handleChange = (e) => {
    setIntext(e.target.value)
  }

  const handleSubmit = (e) => {
    reset()
    e.preventDefault()
    // parameters
    const params = {"text": intext}
    axios
      .post("http://localhost:8080/prediction", params)
      .then((res) => {
        const data = res.data.data
        // const parameters = JSON.stringify(params)
        setOutsong(data.prediction)
        setIssubmit(true)
        // alert(msg)
      })
      .catch((error) => alert(`Error: ${error.message}`))
  }

  const reset = () => {
    setOutsong("")
  }

  return (
    <div className="App">
      <img src={logo} className="App-logo" alt="logo" />
      <p className="App-header">
        ใส่เนื้อเพลงที่คิดถึง
      </p>
      <input
        id="intext"
        type="text"
        value={intext}
        onChange={handleChange}
        placeholder="ฮันนี่ฮันนี่ไอแคนซีเดอะสตาร์ออลเดอะเวฟอมเฮีย"
        className="input"
        size="small"
      />
      <button 
        onClick={handleSubmit} 
        className="button"
      >
        กดเพื่อค้นหา >>
      </button>
      {issubmit && <p className="App-answer">
        {outsong}
      </p>}
    </div>
  );
}

export default App;
