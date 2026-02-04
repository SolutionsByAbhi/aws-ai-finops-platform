 import  type  { NextApiRequest,  NextApiResponse  }  from "next";
 
 export  default async  function  handler(req:  NextApiRequest, res:  NextApiResponse)  {
    const  backendUrl  = process.env.BACKEND_API_URL!;
     const r  =  await  fetch(`${backendUrl}/costs`);
    const  json =  await  r.json();
    res.status(200).json(json);
 }
