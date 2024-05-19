from fastapi import FastAPI, HTTPException, status
import mysql.connector
import schemas
from typing import List
import uuid

app = FastAPI()

host_name = "localhost"
port_number = "3306"
user_name = "root"
password_db = "password"
database_name = "bd_api_pymes"

def connect_to_db():
    return mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

# Obtener todos seguros asociados a las Pymes
@app.get("/pymes", response_model=List[schemas.PymeOutput])
def get_pymes():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT p.*, pr.* FROM Pymes p LEFT JOIN Products pr ON p.pymesId = pr.pymesId ")
    result = cursor.fetchall()
    mydb.close()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Pyme's products found")
    return result

# Obtener seguros de Pyme por su ID 
@app.get("/pymes/{id}", response_model=schemas.PymeOutput)
def get_pyme_with_products(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    
    # Obtener los datos de la Pyme
    cursor.execute("SELECT * FROM Pymes WHERE pymesId = %s", (id,))
    pyme = cursor.fetchone()
    
    if not pyme:
        error_code = "ERR0017"
        error_message = "Error, codigo de seguro invalido"
        trace_id = str(uuid.uuid4())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error-code": error_code, "error-message": error_message, "trace-id": trace_id}
        )
    
    # Obtener los productos asociados a la Pyme
    cursor.execute("SELECT * FROM Products WHERE pymesId = %s", (id,))
    products = cursor.fetchall()
    
    pyme["products"] = products
    mydb.close()
    
    return pyme

# Listar una nueva Pyme
@app.post("/pymes", response_model=schemas.PymeOutput, status_code=status.HTTP_201_CREATED)
def add_pyme(item: schemas.PymeInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    sql = """INSERT INTO Pymes (total_employee, average_age, is_private, bedded, is_sorted_ascending, register_date)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (item.total_employee, item.average_age, item.is_private, item.bedded, item.is_sorted_ascending, item.register_date)
    cursor.execute(sql, val)
    mydb.commit()
    inserted_id = cursor.lastrowid

    # Add coverage information
    coverage_sql = """INSERT INTO Coverage (productId, outpatient_gp, outpatient_sp, outpatient_dental, personal_accident, term_life, critical_illness)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    coverage_val = (inserted_id, item.coverage.outpatient_gp, item.coverage.outpatient_sp, item.coverage.outpatient_dental, item.coverage.personal_accident, item.coverage.term_life, item.coverage.critical_illness)
    cursor.execute(coverage_sql, coverage_val)
    mydb.commit()

    mydb.close()
    return {"pymesId": inserted_id, **item.dict()}

# Modificar una Pyme por su ID
@app.put("/pymes/{id}", response_model=schemas.PymeOutput)
def update_pyme(id: int, item: schemas.PymeInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    sql = """UPDATE Pymes SET total_employee=%s, average_age=%s, is_private=%s, bedded=%s, is_sorted_ascending=%s, register_date=%s
             WHERE pymesId=%s"""
    val = (item.total_employee, item.average_age, item.is_private, item.bedded, item.is_sorted_ascending, item.register_date, id)
    cursor.execute(sql, val)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pyme not found")
    
    # Update coverage information
    coverage_sql = """UPDATE Coverage SET outpatient_gp=%s, outpatient_sp=%s, outpatient_dental=%s, personal_accident=%s, term_life=%s, critical_illness=%s
                      WHERE productId=%s"""
    coverage_val = (item.coverage.outpatient_gp, item.coverage.outpatient_sp, item.coverage.outpatient_dental, item.coverage.personal_accident, item.coverage.term_life, item.coverage.critical_illness, id)
    cursor.execute(coverage_sql, coverage_val)
    mydb.commit()

    mydb.close()
    return {"pymesId": id, **item.dict()}

# Eliminar un Product Pyme por su ID
@app.delete("/pymes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pyme(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Products WHERE productId = %s", (id,))
    mydb.commit()
    mydb.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Pyme not found")
    return {"detail": "Product Pyme deleted successfully"}