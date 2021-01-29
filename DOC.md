**Documentação da API**
----

Através do software Insomnia, o arquivo `ecommerce_insomnia` pode ser importado e o ambiente
para testes estará configurado, de forma que todas as rotas da API estarão disponíveis. <br />
Mais detalhes também podem ser acessados através do navegador, na sua url_base:8000/swagger/ ou /redoc/


**Login**
----
  Gera o token de acesso à API

**Autorização** <br />
  Qualquer usuário

* **URL**

  /api/auth/token/

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "application/x-www-form-urlencoded",
    "cache-control": "no-cache"
  }
  
* **Data Params**

  ``` console
  {
    "grant_type": "password",
    "client_id": "<client id gerado em applications no admin>"
    "client_secret": "<client secret gerado em applications no admin>"
    "username": "test@test.com",
    "password": "123$#45"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** 
    ``` console
    {
      "access_token": "<access_token>",
      "expires_in": 36000,
      "token_type": "Bearer",
      "scope": "read write",
      "refresh_token": "<refresh_token>"
    }
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** 
    ``` console
    {
      "error": "invalid_client"
    }
    
  **Causa: Client id ou client secret diferentes do que foram gerados no admin**

  OU

  * **Code:** 400 BAD REQUEST <br />
    **Content:**
    ``` console
    {
      "error": "invalid_grant",
      "error_description": "Invalid credentials given."
    }
  
  **Causa: Dados de usuário (username ou password) incorretos**
   


**Criar usuário**
----
  Cria usuário para fazer uso da API
 
**Autorização** <br />
  Qualquer usuário

* **URL**

  /api/accounts/

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json"
  }

* **Data Params**

  ``` console
  {
    "username": "test",
    "password1": "#pass123",
    "password2": "#pass123"
  }

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
    ```console
    {
    "id": "<hash uuid>",
    "name": "test"
    }
 
 OBS.: cria um usuário apenas para listar ou detalhar os produtos e categorias
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ``` console
      { 
        error: {
          username: [
              "Usuário com este nome de usuário já existe."
            ]
          },
       }
  
  OU

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ``` console
      {
        error: {<field>:
            [
              "Este campo é obrigatório"
            ]
         },
       }


**Listar usuários**
----
  Lista os usuários
  
**Autorização** <br />
  Qualquer usuário logado terá acesso aos seus dados <br />
  O super usuário pode listar qualquer usuário
 
* **URL**

  /api/accounts/

* **Method:**

  `GET`

* **Data Params**

  None
* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `
    ``` console
    [
      {
        "id": "<hash uuid>",
        "username": "test",
      }
    ]
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Detalhar usuário**
----
  Detalha o usuário

**Autorização** <br />
  Qualquer usuário logado terá acesso aos seus dados <br />
  O super usuário pode detalhar qualquer usuário

* **URL**

  /api/accounts/:id/

* **Method:**

  `GET`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  None
* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `
    ``` console
      {
        "id": "<hash uuid>",
        "username": "test"
      }


 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
  
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID do usuário está incorreto ou não pertence ao usuário (caso não seja super usuário)**
   

**Atualizar usuário**
----
  Atualiza o usuário
 
**Autorização** <br />
  Qualquer usuário logado terá acesso aos seus dados <br />
  O super usuário pode alterar qualquer usuário

* **URL**

  /api/accounts/:id/

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  ``` console
      {
        "username": "new_test"
      }

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
      {
        "id": "<hash uuid>",
        "name": "new_test"
      }

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:**
      ``` console
      {
        "<field>": [
            "Este campo é obrigatório."
        ]
      }
     
   **Os campos no detalhe não foram informados**
    
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID do usuário está incorreto ou não pertence ao usuário (caso não seja super usuário)**
 
 

**Excluir usuário**
----
  Exclui um usuário.
 
 
**Autorização** <br />
  Qualquer usuário logado terá acesso aos seus dados <br />
  O super usuário pode excluir qualquer usuário

* **URL**

  /api/accounts/:id/

* **Method:**

  `DELETE`
  
*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204 NO CONTENT<br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe
  

  OU

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Criar categoria**
----
  Cria uma categoria
 
**Autorização** <br />
  Apenas o super usuário pode criar categorias

* **URL**

  /api/category/

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Data Params**

  ``` console
  {
    "name": "cat 03",
    "parent": "e2a2d8d5-1fa1-46b1-aa55-d3d962795a2a"
  }

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
    ```console
    {
      "id": "74b03a3d-7ac8-46b1-9951-cd5d4fc68e6f",
      "name": "cat 03",
      "slug": "cat-03",
      "parent": "e2a2d8d5-1fa1-46b1-aa55-d3d962795a2a"
    } 
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ´´´ console
      {
        "error": {
          "<field>": [
            "Este campo é obrigatório"
            ]
        }
      }

  OU
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }

   **Causa: Token informado está expirado ou inválido**

**Listar categorias**
----
  Lista as categorias

**Autorização** <br />
  Qualquer usuário logado terá acesso aos dados
 
* **URL**

  /api/category/

* **Method:**

  `GET`

* **Data Params**

  None
  
* **URL Params**

  * search=<sua pesquisa>: pesquisa a categoria baseada no slug ou no nome
  * <field>=<seu filtro para o campo digitado>: faz um filtro no campo digitado com o valor inserido
  * page-x: o número da página que vc quer ter acesso às categorias

* **Headers**
  ``` console
  {
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console  
    {
      "count": 3, # número de resultados
      "next": null,
      "previous": null,
      "results": [
        {
          "id": "<hash uuid>",
          "name": "cat test 01",
          "slug": "cat-test-01",
          "parent": null
         },
         {
          "id": "<hash uuid>",
          "name": "cat test 02",
          "slug": "cat-test-02",
          "parent": <hash uuid da catogria anterior>
         },
         {
          "id": "<hash uuid>",
          "name": "cat test 03",
          "slug": "cat-test-03",
          "parent": <hash uuid da catogria anterior>
         }
      ]
    }
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Detalhar categoria**
----
  Detalha a categoria

**Autorização** <br />
  Qualquer usuário logado terá acesso aos dados

* **URL**

  /api/category/:id/

* **Method:**

  `GET`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`
 
* **Data Params**

  None
* **Headers**
  ``` console
  {
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "name": "cat 01",
      "slug": "cat-01",
      "parent": null
    }
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
 
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe**
 

**Atualizar categoria**
----
  Atualiza a categoria
  
**Autorização** <br />
  Apenas o super usuário pode atualizar categorias

* **URL**

  /api/category/:id/

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  ``` console
      {
      "name": "cat 02",
      "parent": <uuid de outra categoria>
      }

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "name": "cat 01",
      "slug": "cat-01",
      "parent": null
    }

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:**
      ``` console
      {
        "<field>": [
            "Este campo é obrigatório."
        ]
      }
     
   **Os campos no detalhe não foram informados**
    
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe


**Atualizar categoria**
----
  Atualiza a categoria
 
**Autorização** <br />
  Apenas o super usuário pode atualizar categorias
 
* **URL**

  /api/category/:id/

* **Method:**

  `PATCH`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  ``` console
      {
      "name": "cat 02",
      "parent": <uuid de outra categoria>
      }

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "name": "cat 01",
      "slug": "cat-01",
      "parent": null
    }

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
    
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe

 

**Excluir categoria**
----
  Exclui uma categoria.
 
**Autorização** <br />
  Apenas o super usuário pode excluir categorias
 
* **URL**

  /api/category/:id/

* **Method:**

  `DELETE`
  
*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204 NO CONTENT<br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe
  

  OU

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Criar produto**
----
  Cria um produto

**Autorização** <br />
  Apenas o super usuário pode criar produtos

* **URL**

  /api/product/

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "multipart/form-data",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Data Params**

  ``` console
  {
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 111,
      "image": "<url da imagem>"
   }

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
    ```console
    {
      "id": "<hash uuid>",
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "slug": "teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 111,
      "image": "<url da imagem>"
    }
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ´´´ console
      {
        "error": {
          "<field>": [
            "Este campo é obrigatório"
            ]
        }
      }

  OU
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }

   **Causa: Token informado está expirado ou inválido**

**Listar produtos**
----
  Lista os produtos

**Autorização** <br />
  Qualquer usuário logado terá acesso aos dados

* **URL**

  /api/product/

* **Method:**

  `GET`

* **Data Params**

  None
  
* **URL Params**

  * search=<sua pesquisa>: pesquisa a categoria baseada no slug ou no nome
  * <field>=<seu filtro para o campo digitado>: faz um filtro no campo digitado com o valor inserido
  * page-x: o número da página que vc quer ter acesso às categorias

* **Headers**
  ``` console
  {
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console  
    {
      "count": 2,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": "<hash uuid>",
          "category": "<hash uuid da categoria>",
          "name": "Teste 01",
          "slug": "teste-01",
          "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
          "value": "12.15",
          "stock": 8,
          "image": "<url da imagem>"
         },
         {
          "id": "<hash uuid>",
          "category": "null",
          "name": "Teste 01",
          "slug": "teste-01",
          "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
          "value": "12.15",
          "stock": 81,
          "image": "<url da imagem>"
         }
        ]
      }
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Detalhar produto**
----
  Detalha o produto

**Autorização** <br />
  Qualquer usuário logado terá acesso aos dados

* **URL**

  /api/product/:id/

* **Method:**

  `GET`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`
 
* **Data Params**

  None
* **Headers**
  ``` console
  {
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "category": "null",
      "name": "Teste 01",
      "slug": "teste-01",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 81,
      "image": "<url da imagem>"
     }
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
 
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da produto está incorreto ou não existe**
 

**Atualizar produto**
----
  Atualiza o produto

**Autorização** <br />
  Apenas o super usuário pode atualizar produtos

* **URL**

  /api/product/:id/

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  ``` console
   {
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 111,
      "image": "<url da imagem>"* **Code:** 400 UNAUTHORIZED <br />
   }

* **Headers**
  ``` console
  {
    "Contet-Type": "multipart/form-data",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "category": "null",
      "name": "Teste 01",
      "slug": "teste-01",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 81,
      "image": "<url da imagem>"
     }

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:**
      ``` console
      {
        "<field>": [
            "Este campo é obrigatório."
        ]
      }
     
   **Os campos no detalhe não foram informados**
    
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID da categoria está incorreto ou não existe


**Atualizar produtos**
----
  Atualiza o produto

**Autorização** <br />
  Apenas o super usuário pode atualizar produtos

* **URL**

  /api/product/:id/

* **Method:**

  `PATCH`

*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  ``` console
  {
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 111,
      "image": "<url da imagem>"
   }

* **Headers**
  ``` console
  {
    "Contet-Type": "multipart/form-data",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
    ``` console
    {
      "id": "<hash uuid>",
      "category": "null",
      "name": "Teste 01",
      "slug": "teste-01",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 81,
      "image": "<url da imagem>"
     }

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**
    
  OU
  
  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID do produto está incorreto ou não existe

 

**Excluir produto**
----
  Exclui um produto.

**Autorização** <br />
  Apenas o super usuário pode excluir produtos
 
* **URL**

  /api/product/:id/

* **Method:**

  `DELETE`
  
*  **URL Params**

   **Required:**
 
   `id=[<uuid>]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204 NO CONTENT<br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      {
        "detail": "Not found."
      }
     
   **Causa: ID do produto está incorreto ou não existe
  

  OU

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }
     
   **Causa: Token informado está expirado ou inválido**


**Adiconar ao estoque**
----
  Adiciona mais produtos ao estoque

**Autorização** <br />
  Apenas o super usuário pode adiconar produtos

* **URL**

  /api/product/add_stock

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Data Params**

  ``` console
  {
	  "product": "<hash uuid>",
	  "quantity": 27
   }

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
    ```console
    {
      "id": "<hash uuid>",
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "slug": "teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 138,
      "image": "<url da imagem>"
    }
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ´´´ console
      {
        "error": {
          "<field>": [
            "Este campo é obrigatório"
            ]
        }
      }

  OU
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }

   **Causa: Token informado está expirado ou inválido**
   
   OU
   
   * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      [
        "Produto não encontrado"
      ]
     
   **Causa: ID do produto está incorreto ou não existe
   
   
**Remover do estoque**
----
  Remove produto do estoque (venda)

**Autorização** <br />
  Apenas o super usuário pode remover produtos
 
* **URL**

  /api/product/remove_stock

* **Method:**

  `POST`

* **Headers**
  ``` console
  {
    "Contet-Type": "application/json",
    "Authorization": "Bearer <access_token gerado no login>"
  }

* **Data Params**

  ``` console
  {
	  "product": "<hash uuid>",
	  "quantity": 27
   }

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
    ```console
    {
      "id": "<hash uuid>",
      "category": "<hash uuid da categoria>",
      "name": "Teste",
      "slug": "teste",
      "description": "Lorem ipsum dore Lorem ipsum dore Lorem ipsum dore",
      "value": "12.15",
      "stock": 111,
      "image": "<url da imagem>"
    }
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    ´´´ console
      {
        "error": {
          "<field>": [
            "Este campo é obrigatório"
            ]
        }
      }

  OU
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:**
      ``` console
      {
        "detail": "Authentication credentials were not provided."
      }

   **Causa: Token informado está expirado ou inválido**
   
   OU
   
   * **Code:** 404 NOT FOUND <br />
    **Content:**
      ``` console
      [
        "Produto não encontrado"
      ]
     
   **Causa: ID do produto está incorreto ou não existe
   
   OU
   
   * **Code:** 400 BAD REQUEST <br />
    **Content:**
      ``` console
      [
        "Quantidade insuficiente"
      ]
     
   **Causa: A quantidade do produto não é suficiente para esta retirada**
