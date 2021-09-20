WITH SENDS as
(
select 
       case when  (    (
                        lower(br.Template_name)         like '%fjsjsd%'       or
                        lower(br.Template_name)         like '%adfnkl%'          or
                        lower(br.Template_name)         like '%psdfjs%'          or
                        lower(br.Template_name)         like '%sdfoijsd%'     or
                        lower(br.Template_name)         like '%dosdjf%'      or
                        )
                        and
                        (
                        lower(br.Template_name)         not like '%sdfsdf%'
                    and lower(br.Template_name)         not like '%ssdf%'
                    and lower(br.Template_name)         not like '%uijs%'        
                        ) 
                   ) 
                   then 'product 1'


             
             when  (
                   lower(br.Template_name) like '%sdffe%'
               or  lower(br.Template_name) like '%sdssc%'
               or  lower(br.Template_name) like '%dwwfrf%'
                   )
               then 'product 2'
                    
             when  (
                   lower(br.Template_name) like '%ipjnin%'
                   )      
               then 'product 3'
               
             when (
                   (
                   lower(br.Template_name) like '%weryuih%'
               or  lower(br.Template_name) like '%hjhjhj%' 
               or  lower(br.Template_name) like '%jkjkh%' 
               or  lower(br.Template_name) like '%uihiuh%'
                   ) and
                   (
                   lower(br.Template_name) not like '%fdgdffdg%'
               and lower(br.Template_name) not like '%dfgdfg%'
               and lower(br.Template_name) not like '%dfgdgdf%' 
                   )
                  ) 
               then 'product 4'                    
        
        else 'product 5' 
        end as Product_group,
                --lifestage, 
                lower(br.Template_name) as template,        
                br.campaign_code,
                date_part(month, br.broadcast_date):: integer as month_of_send, 
                date_part(year, br.broadcast_date):: integer  as year_of_send, 
                count(distinct br.broadcast_date) as Number_of_sends,
                case when Number_of_sends > 3 then Number_of_sends else 0 end as Automated_or_Manual
                
                
FROM            broadcast_table.delivery_sends br

left join       accounts_table   acc on      br.account = acc.account
 
where br.broadcast_date >= '{@start_date}'::DATETIME --'2021-01-01' --python Parameters
and   br.broadcast_date <  '{@end_date}'  ::DATETIME --'2022-01-01' --python Parameters



group by 1,2,3,4,5
--end;

)

, Campaigns as (

select 
        product_group,
        case when Number_of_sends > '{@send_for_automated}'::integer /* --python Parameters */         then 'Automated'  
             else 'Manual'
        End as Automated_Status,
        month_of_send,
        year_of_send, 
        
        case when       template like '%campaign_a%'                                    then 'Campaign A'
             when       template like '%campaign_b%'                                    then 'Campaign B'
             when       template like '%campaign_c%'                                    then 'Campaign C'
             when       template like '%campaign_d%'                                    then 'Campaign D'
             when       template like '%campaign_e%'                                    then 'Campaign E'
             when       template like '%campaign_f%'                                    then 'Campaign F'
             when       template like '%campaign_g%'                                    then 'Campaign G'
             when       template like '%campaign_h%'                                    then 'Campaign H'
             when       template like '%campaign_i%'                                    then 'Campaign I'
             when       template like '%campaign_j%'                                    then 'Campaign J'
             when       template like '%campaign_k%'                                    then 'Campaign K'
             when       template like '%campaign_l%'                                    then 'Campaign L'
             when       template like '%campaign_m%'                                    then 'Campaign M'
             when       template like '%campaign_n%'                                    then 'Campaign N'
             when       template like '%campaign_o%'                                    then 'Campaign O'
             ------
             /* additional 20-40 case when statements added now  to group campaigns 
                but they aren't shown in this blog post for certain reasons 
                including data confidentiality                
                
                but you understand the premise to how the data is being cleaned
                
             */             
             -----
             
             when       template like '%campaign_bn%'                                   then 'Campaign BN'
   
             else template -- if there aren't multiple templates with similar names, then bring through the individual template
             end as Campaigns,
 
        
        case when Automated_Status = 'Automated'        then 1 else 0 end as Automated_sends,
        case when Automated_Status = 'Manual'           then 1 else 0 end as Manual_sends,
        sum(Number_of_sends) as total_broadcast_sends -- This is adding all the sends of each template together if they are grouped into one campaign e.g. scratchcard 
    
        
from 
        
SENDS
        
group by 1,2,3,4,5

order by total_broadcast_sends desc

)

select
        product_group,
        month_of_send,
        year_of_send, 
        
        count(total_broadcast_sends)    as sends_per_project,
        sum(Automated_sends)            as number_of_automated_sends,
        sum(Manual_sends)               as number_of_manual_sends,
        
        round(100*(cast(number_of_automated_sends::float/nullif(count(total_broadcast_sends),0)  as numeric(36,2))),0)  as Percentage_of_Campaigns_Automated,
        round(cast(number_of_manual_sends::float/nullif(number_of_automated_sends,0) as numeric(36,2)), 2)              as Manual_Automated_Ratio               
        -- ratio of how many manual campaigns for every automated one --

        
        from 
        
        Campaigns
        
        group by 1,2,3