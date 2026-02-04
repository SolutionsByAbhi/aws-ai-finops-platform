import  Link  from  "next/link";

export  default  function Home()  {
   return  (
       <main  style={{ padding:  "2rem"  }}>
          <h1>AWS  AI  FinOps Dashboard</h1>
           <p>AI‑powered cost  insights  and  optimization recommendations.</p>
           <ul>
             <li><Link  href="/costs">View  Costs</Link></li>
              <li><Link href="/recommendations">View  Recommendations</Link></li>
          </ul>
       </main>
   );
}
