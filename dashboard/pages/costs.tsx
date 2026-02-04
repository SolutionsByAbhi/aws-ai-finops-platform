import  {  useEffect,  useState }  from  "react";

type  CostRow  =  { date:  string;  service:  string; cost:  number  };

export  default  function  CostsPage() {
    const [rows,  setRows]  =  useState<CostRow[]>([]);

    useEffect(() =>  {
       fetch("/api/costs")
          .then((r)  =>  r.json())
          .then((d)  => setRows(d.items  ||  []));
   },  []);

   return  (
      <main  style={{  padding:  "2rem" }}>
           <h1>Daily Costs</h1>
           <table>
             <thead>
                  <tr>
                    <th>Date</th><th>Service</th><th>Cost  (USD)</th>
                 </tr>
              </thead>
              <tbody>
                 {rows.map((r,  i)  => (
                     <tr  key={i}>
                        <td>{r.date}</td>
                        <td>{r.service}</td>
                         <td>{r.cost.toFixed(2)}</td>
                    </tr>
                  ))}
             </tbody>
           </table>
      </main>
    );
}
