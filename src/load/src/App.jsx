import { useState, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_URL_EP
const HEALTH_INTERVAL_MS = 1000
const HEALTH_TIMEOUT_MS = 60000

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [apiReady, setApiReady] = useState(false)
  const [apiTimeout, setApiTimeout] = useState(false)

  useEffect(() => {
    let elapsed = 0
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/health`)
        if (res.ok) {
          setApiReady(true)
          clearInterval(interval)
        }
      } catch (_) {
        // API not yet available
      }
      elapsed += HEALTH_INTERVAL_MS
      if (elapsed >= HEALTH_TIMEOUT_MS) {
        clearInterval(interval)
        setApiTimeout(true)
      }
    }, HEALTH_INTERVAL_MS)
    return () => clearInterval(interval)
  }, [])

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

  if (!apiReady && !apiTimeout) {
    return (
      <div className="container">
        <h1>Clasificador de Residuos</h1>
        <p className="subtitle">RealWaste - InceptionV3</p>
        <div className="api-loading">
          <div className="spinner" />
          <p>Conectando con la API...</p>
        </div>
      </div>
    )
  }

  if (apiTimeout) {
    return (
      <div className="container">
        <h1>Clasificador de Residuos</h1>
        <p className="subtitle">RealWaste - InceptionV3</p>
        <div className="api-error">
          <p>No se pudo conectar con la API. Verifica que el servicio esté activo e intenta recargar la página.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>Clasificador de Residuos</h1>
      <p className="subtitle">RealWaste - InceptionV3</p>
      <p className="instructions">A continuación, encontrarás un modelo entrenado para clasificar tus residuos en las siguientes categorías: Cartón, Residuos Orgánicos, Vidrio, Metal, Basura Miscelánea, Papel, Plástico, Residuos Textiles y Vegetación.</p>
      <p className="instructions">Para mejores resultados, asegúrate de que la imagen esté bien iluminada, enfocada y que <b>el fondo sea blanco</b>.</p>
      
      <div className="upload-area">
        {preview ? (
          <img src={preview} alt="Preview" className="preview" />
        ) : (
          <span>Selecciona o toma una foto</span>
        )}
      </div>

      <div className="actions">
        <label className="btn btn-secondary">
          Galeria
          <input type="file" accept="image/*" onChange={handleFileChange} />
        </label>
        <label className="btn btn-secondary">
          Camara
          <input type="file" accept="image/*" capture="environment" onChange={handleFileChange} />
        </label>
        <button className="btn btn-primary" onClick={handleSubmit} disabled={!file || loading}>
          {loading ? 'Clasificando...' : 'Clasificar'}
        </button>
      </div>

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
