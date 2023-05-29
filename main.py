
from fastapi import FastAPI, Body, Path, Query,Request, HTTPException,Depends

# Esta clase se utiliza para enviar la respuesta en html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials

#Esta libreria nos ayuda a validar datos 
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
 

app = FastAPI()

#Cambia el titulo de la documentacion antes estaba 'FastAPI'
app.title ='Mi aplicacion'
#Cambia la version de la documentacion antes estaba '0.1.0'
app.version = '0.1.1' 

#Esquema 
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5,max_length=15)
    overview: str
    year: int = Field(ge=1990,le=2022)
    rating: float
    category: str

#Para los datos por defetas la clase de debe llamar Config
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title": "mi pelicula",
                "overview": "Descripcion de la pelicula ",
                "year":2022,
                "rating":9.8,        
                "category": "Accion"        
    
            }
        }

class User(BaseModel):
    email: str
    password: str

'''
La clase JWTBearer es creada para verifica la autelenticidad del token 

'''
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request): 
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email']!= "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        

movies = [
    {
        "id":1,
        "title": "Avatar",
        "overview": "Em un exuberante planeta llamado Pandora viven ",
        "year":2009,
        "rating":7.8,        
        "category": "Accion"        
    },
    {
        "id":2,
        "title": "Rambo",
        "overview": "Batalla en la selva",
        "year":1982,
        "rating":9,        
        "category": "Accion"        
    },
    {
        "id":3,
        "title": "Toy Story",
        "overview": "Historia de jugetes en una casa",
        "year":1995,
        "rating":8.5,        
        "category": "Animada"        
    }

]



#Ruta
#Se añada una nueva etiqueta 'Home' con tags, antes estaba 'dafault'

@app.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = str = create_token(user.dict())
        return JSONResponse(status_code=200,content= token)

@app.get('/', tags=['home'])
def  message():
    return HTMLResponse('<h1>hello world!</h1>')

#Rutas de peliculas
# Metodo get sencillo
'''
@app.get('/movies',tags=['movies'])
def get_movies():
    return movies
'''

# Utilizando la clase JSONResponse
# response_model se utiliza para especificar que dipode datos se va devolver
@app.get('/movies',tags=['movies'],status_code=200, response_model=List[Movie])
def get_movies()-> List[Movie]:
    return JSONResponse (status_code=200, content=movies)


#Ruta pasandole un parameto para filtro
#Validando el parametro id
'''
@app.get('/movies/{id}', tags=['movies'])
def get_movies_parametro(id: int):

    for item in movies:
        if item['id']==id:

            return item

    return "No encontro la pelicula"

'''

@app.get('/movies/{id}', tags=['movies'])
def get_movies_parametro(id: int = Path(ge=1,le=2000)):

    for item in movies:
        if item['id']==id:

            return item

    return "No encontro la pelicula"


#Ruta pasandole un Query para filtro
#sin validacion de query
'''
@app.get('/movies/',tags=['movies'])
def get_movies_by_query(category: str):

    for peli in movies:
        if peli['category']==category:
            return peli
    return "No se encontro pelicula"

'''    
#Validacion de query
@app.get('/movies/',tags=['movies'])
def get_movies_by_query(category: str = Query(min_length=5,max_length=15)):

    for peli in movies:
        if peli['category']==category:
            return peli
    return "No se encontro pelicula"

'''
Clase 8/19
Metodo POST con clase de esquema
'''

@app.post('/movies',tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)

    return movies


'''

@app.post('/movies',tags=['movies'])
def create_movie(id: int = Body(),title: str = Body(),overview: str = Body(),year: int = Body(),year: float = Body(),category: str = Body()):
    movies.append({
        "id":id,
        "title": title,
        "overview": "overview,
        "year":year,
        "rating":rating,        
        "category": category 
    })

    return movies

'''

#Eliminar datos por id
@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id']==id:
            movies.remove(item)
            return movies





#Actualizar datos
@app.put('/movies/{id}',tags=['movies'])
def put_monies(id: int, movie: Movie):
    for item in movies:
        if item['id']==id:
            
            item['title']=movie.title
            item['overview']=movie.overview
            item['year']=movie.year
            item['rating']=movie.rating
            item['category']=movie.category             
            return movies



'''
Esta ruta estara bloqueada por un token
'''
@app.get('/movies',tags=['Token'],status_code=200, response_model=List[Movie],dependencies=[Depends(JWTBearer)])
def get_movies()-> List[Movie]:
    return JSONResponse (status_code=200, content=movies)