import {  useEffect,  useState  } from  "react";

export default  function  RecommendationsPage()  {
   const  [items, setItems]  =  useState<any[]>([]);

   useEffect(()  => {
       fetch("/api/recommendations")
          .then((r)  =>  r.json())
          .then((d)  =>  setItems(d.items ||  []));
   },  []);

   return  (
       <main style={{  padding:  "2rem"  }}>
          <h1>AI  Recommendations</h1>
          {items.map((item,  idx) =>  (
              <section  key={idx} style={{  border:  "1px  solid #ddd",  marginBottom:  "1rem",  padding: "1rem"  }}>
                 <h3>{item.id}</h3>
                  {(item.recommendations ||  []).map((r:  any,  i: number)  =>  (
                     <div key={i}  style={{  marginBottom:  "0.5rem" }}>
                         <strong>{r.title}</strong> —  {r.description}
                        <div>Estimated  savings:  ${r.estimated_savings_usd}  | Priority:  {r.priority}</div>
                     </div>
                 ))}
              </section>
          ))}
       </main>
   );
}
