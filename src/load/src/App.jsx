import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_URL_EP

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (!selected) return
    setFile(selected)
    setPreview(URL.createObjectURL(selected))
    setResult(null)
    setError(null)
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setResult(await res.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Clasificador de Residuos</h1>
      <p className="subtitle">RealWaste - InceptionV3</p>

      <label className="upload-area">
        {preview ? (
          <img src={preview} alt="Preview" className="preview" />
        ) : (
          <span>Haz clic o arrastra una imagen</span>
        )}
        <input type="file" accept="image/*" onChange={handleFileChange} />
      </label>

      <button onClick={handleSubmit} disabled={!file || loading}>
        {loading ? 'Clasificando...' : 'Clasificar'}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <p><strong>{result.class_name_es}</strong> ({result.class_name})</p>
          <p>Confianza: {(result.confidence * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App
