import './App.css';
import { useState } from 'react'
import axios from 'axios'

function App() {
  const [mail, setMail] = useState('')
  const [res, setRes] = useState('Enter mail')

  const spamMail = (e) => {
    e.preventDefault()
    axios.post('https://ramfr.herokuapp.com/api',{message:mail})
    .then((res) => {
      // console.log(res);
      setRes(res.data)
      setMail('')
    })
  }

  return (
    <div className="App">
      <form>
        <input required type="text" onChange={(e) => setMail(e.target.value)} value={mail} placeholder="enter the mail" />
        <button onClick={spamMail}>check</button>
      </form>
      <h6>{res}</h6>
    </div>
  );
}

export default App;
