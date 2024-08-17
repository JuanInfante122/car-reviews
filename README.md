# **Proyecto de Análisis de Opiniones de Automóviles**

Este proyecto consiste en una aplicación web que realiza scraping de opiniones sobre automóviles, las analiza utilizando técnicas de Inteligencia Artificial (IA), y presenta los resultados visualmente. La aplicación está desarrollada con Flask para el backend y React para el frontend.

## **Índice**

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Instrucciones de Instalación y Ejecución](#instrucciones-de-instalación-y-ejecución)
3. [Técnicas de IA Utilizadas](#técnicas-de-ia-utilizadas)
4. [Librerías y Dependencias](#librerías-y-dependencias)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Contribución](#contribución)
7. [Licencia](#licencia)

## **Descripción del Proyecto**

La aplicación web permite a los usuarios obtener opiniones sobre diferentes modelos de automóviles, analizar el sentimiento de estas opiniones, y generar resúmenes automáticos. La interfaz de usuario permite filtrar los automóviles por marca y visualizar los resultados de forma intuitiva.

### **Características Principales**

- **Scraping de Opiniones**: Recopila opiniones de un sitio web específico sobre automóviles.
- **Análisis de Sentimientos**: Utiliza VADER para analizar el sentimiento de las opiniones.
- **Resumen Automático**: Genera un resumen de las opiniones usando TextRank.
- **Interfaz de Usuario**: Permite filtrar y mostrar los automóviles por marca utilizando React.

## **Instrucciones de Instalación y Ejecución**

### **Requisitos**

- Python 3.x
- Node.js y npm (para el frontend)
- Acceso a internet para realizar scraping

### **Backend (Flask)**

1. **Clonar el Repositorio**

```bash
   git clone https://github.com/JuanInfante122/car-reviews.git
   cd car-reviews
```


2. **Instalar Dependencias**

- Crea un entorno virtual y activa:

```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
```

- Instala las dependencias:

```bash
    pip install -r requirements.txt
```

- Navega al directorio donde esta el backend:

```bash
   cd backend
```

- Ejecutar el servidor:

```bash
    python main.py
```

El backend se ejecutará en http://localhost:5000.

### **Frontend (React)**

1. **Instalar Dependencias**

- Navega al directorio donde esta el front:

```bash
   cd ..
   cd frontend
```

- Instala las dependencias:

```bash
   npm install
```

- Ejecutar la Aplicacion:

```bash
   npm start
```

### **Técnicas de IA Utilizadas**

**Análisis de Sentimientos**

VADER (Valence Aware Dictionary and sEntiment Reasoner): Es una herramienta de análisis de sentimientos que utiliza un diccionario léxico y una serie de reglas heurísticas para analizar el sentimiento en textos. Se utiliza para categorizar las opiniones como positivas, negativas o neutrales en función del puntaje de sentimiento.

**Resumen Automatico**

TextRank: Un algoritmo de resumen basado en el modelo de PageRank. Este modelo clasifica las oraciones en un texto para determinar cuáles son las más importantes y generar un resumen coherente. Utiliza el análisis de texto y el cálculo de la similitud entre las oraciones para producir el resumen


### **Librerias y Dependencias**

**Backend**

- Flask: Framework web para Python. (Instalación: pip install Flask)
- requests: Para realizar solicitudes HTTP. (Instalación: pip install requests)
- BeautifulSoup: Para el scraping de contenido web. (Instalación: pip install beaautifulsoup4)
- vaderSentiment: Herramienta para el análisis de sentimientos. (Instalación: pip install vaderSentiment)
- nltk: Biblioteca para procesamiento de lenguaje natural. (Instalación: pip install nltk)
- sumy: Para el resumen automático de texto. (Instalación: pip install sumy)

**Frontend**

- React: Biblioteca para la construcción de interfaces de usuario. (Instalación: npx create-react-app frontend)
- axios: Para realizar solicitudes HTTP desde el frontend. (Instalación: npm install axios)

## **Manejo de Errores y Casos Extremos**

En esta sección se describen los posibles errores y casos extremos que puedes encontrar durante el desarrollo y uso de la aplicación, así como las estrategias para manejarlos.

### **Errores Comunes y Soluciones**

#### **1. Problemas con las Peticiones de API**

**Error**: `Cannot access 'mockCars' before initialization`

- **Descripción**: Este error indica que el nombre del modelo de los automóviles (`mockCars`) no está correctamente inicializado o se está accediendo antes de que se haya definido.
- **Solución**: Asegúrate de que todas las variables estén correctamente inicializadas antes de ser utilizadas. Revisa la secuencia de ejecución en los hooks de React (`useEffect`) para garantizar que las dependencias están correctamente configuradas.

#### **2. Problemas de CORS (Cross-Origin Resource Sharing)**

**Error**: `Access to fetch at 'http://localhost:5000/api/opinions' from origin 'http://localhost:3000' has been blocked by CORS policy`

- **Descripción**: El navegador bloquea las solicitudes de origen cruzado debido a políticas de seguridad CORS.
- **Solución**: Para solucionar problemas de CORS, asegúrate de que el servidor backend permite solicitudes desde el origen del frontend. Puedes agregar el siguiente código a tu configuración de Flask:

    ```python
    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app)
    ```

  Esto habilita CORS para todas las rutas. Para una configuración más segura, puedes restringir los orígenes permitidos:

    ```python
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    ```

#### **3. Errores en la API**

**Error**: `404 Not Found` o `500 Internal Server Error`

- **Descripción**: Estos errores indican que la solicitud a la API no pudo completarse. Un `404` significa que la ruta solicitada no existe, mientras que un `500` indica un problema en el servidor.
- **Solución**: Verifica la URL de la API y asegúrate de que el backend esté en funcionamiento. Revisa los logs del servidor Flask para identificar el problema específico.

#### **4. Errores en el Procesamiento de Datos**

**Error**: `TypeError: Cannot read property 'summary' of undefined`

- **Descripción**: Este error ocurre cuando el frontend intenta acceder a una propiedad que no está definida en la respuesta de la API.
- **Solución**: Asegúrate de que la estructura de los datos recibidos de la API coincida con lo esperado. Verifica la respuesta en la herramienta de desarrollo del navegador y ajusta el frontend para manejar datos incompletos o errores.

### **Manejo de Casos Extremos**

#### **1. No Hay Opiniones Disponibles**

**Descripción**: La API puede devolver menos opiniones de las esperadas, o ninguna opinión.
- **Solución**: Implementa lógica en el frontend para manejar estos casos. Muestra un mensaje amigable al usuario si no hay opiniones disponibles.

    ```javascript
    {loading ? (
      <p>Loading...</p>
    ) : (
      cars.length > 0 ? (
        <CarList cars={selectedBrand ? cars.filter(car => car.brand === selectedBrand) : cars} />
      ) : (
        <p>No cars available for the selected brand.</p>
      )
    )}
    ```

#### **2. Errores en el Análisis de Sentimientos**

**Descripción**: El análisis de sentimientos puede fallar si las opiniones están mal formateadas o contienen caracteres especiales.
- **Solución**: Implementa manejo de errores en el backend para capturar y registrar excepciones durante el análisis de sentimientos. Asegúrate de validar y limpiar el texto antes de procesarlo.

    ```python
    def analyze_sentiments(opinions):
        sentiments = []
        for opinion in opinions:
            try:
                cleaned_opinion = clean_text(opinion)
                sentiment = analyzer.polarity_scores(cleaned_opinion)
                sentiment_score = sentiment['compound']
                if sentiment_score > 0.1:
                    sentiment_label = 'Positivo'
                elif sentiment_score < -0.1:
                    sentiment_label = 'Negativo'
                else:
                    sentiment_label = 'Neutral'
                sentiments.append((opinion, sentiment_label, sentiment_score))
            except Exception as e:
                print(f"Error analyzing sentiment: {e}")
                sentiments.append((opinion, 'Error', 0))
        return sentiments
    ```

#### **3. Problemas de Red y Tiempo de Espera**

**Descripción**: Las solicitudes a la API pueden fallar debido a problemas de red o tiempos de espera prolongados.
- **Solución**: Implementa manejo de tiempos de espera y reintentos en las solicitudes del frontend. Usa la funcionalidad `timeout` de `fetch` y considera utilizar una biblioteca como `axios` que soporta reintentos.

    ```javascript
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch(`http://localhost:5000/api/opinions?model=${car.brand.toLowerCase()}/${car.model.toLowerCase()}`, { timeout: 5000 });
          if (!response.ok) throw new Error('Network response was not ok');
          const data = await response.json();
          setCars((prevCars) =>
            prevCars.map((prevCar) =>
              prevCar.model === car.model ? { ...prevCar, summary: data.summary } : prevCar
            )
          );
          setLoading(false);
        } catch (error) {
          console.error('Error fetching summary:', error);
        }
      };
      
      fetchData();
    }, []);
    ```

### **Consejos Adicionales**

- **Revisa los Logs**: Los logs del navegador y del servidor pueden proporcionar información valiosa sobre los errores y problemas de la aplicación.
- **Pruebas Unitarias**: Considera agregar pruebas unitarias para asegurar que las funciones de análisis y resumen manejen casos extremos correctamente.



Credit: [JuanInfante122](https://github.com/JuanInfante122) Last Edit on 18/08/2024