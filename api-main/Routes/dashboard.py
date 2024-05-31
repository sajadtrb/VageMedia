from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Utils.csvWorld import load_csv
import pycountry
import uuid


router = APIRouter()

@router.get("/test")
async def test():
    return {"Hello": "test"}

@router.get("/artists")
async def artists():
    data = load_csv()
    # process data
    artists = data['Asset Artist'].unique().tolist()

    artist_data = []
    for artist in artists:
        artist_info = {
            "artist_name": artist,
            "uid": str(uuid.uuid4()),
            "image": "default.jpg"
        }
        artist_data.append(artist_info)
    # end process data
    return {
        "total_artists": len(artists),
        "artists": artist_data
    }

@router.get("/platforms")
async def platforms():
    data = load_csv()

    # Grouping by platform (DSP)
    grouped_platforms = data.groupby('DSP')

    # Preparing the output dictionary
    output = {
        'total_platforms': len(grouped_platforms),
        'platforms': []
    }

    # Iterating through each group to populate the platforms list
    for name, group in grouped_platforms:
        platform_data = {
            'id': str(uuid.uuid4()),
            'title': name,
            'view': float(group['Quantity'].sum()),
            'revenue': float(group['Sale net receipts'].sum()),
            'last_update': str(group['Sale End date'].max()),
            'image': 'default.jpg',
            'artists': []
        }

        # Grouping by artists within each platform
        grouped_artists = group.groupby('Asset Artist')
        for artist_name, artist_group in grouped_artists:
            artist_data = {
                'id': str(uuid.uuid4()),
                'title': artist_name,
                'revenue': float(artist_group['Sale net receipts'].sum()),
                'view': float(artist_group['Quantity'].sum()),
                'image': 'default.jpg'
            }
            platform_data['artists'].append(artist_data)

        output['platforms'].append(platform_data)
        
    #end process data
    return JSONResponse(content=output)

@router.get("/statistics")
async def statistics():
    data = load_csv()
    # process data
    net_income = data['Reported Royalty'].sum()
    total = data['Sale net receipts'].sum()
    profit = net_income
    paid = 0
    
    return JSONResponse(content={
        "net_income": float(net_income),
        "total": float(total),
        "profit": float(profit),
        "paid": float(paid)
    })

@router.get("/top_activities")
async def top_activities():
    data = load_csv()
    # process data
    grouped_artists = data.groupby('Asset Artist')
    output = {
        'data': []
    }
    for artist_name, artist_group in grouped_artists:
        artist_data = {
            'artist': {
                'id': str(uuid.uuid4()),
                'image': 'default.jpg',
                'title': artist_name,
                'started_at': str(artist_group['Sale Start date'].min()),
                'view': float(artist_group['Quantity'].sum()),
                'revenue': float(artist_group['Sale net receipts'].sum())
            },
            'products': []
        }
        # Grouping products for each artist
        grouped_products = artist_group.groupby('Asset ISRC')
        for ISRC, product_group in grouped_products:
            product_data = {
                'id': str(uuid.uuid4()),  # Generating a fake UUID
                'view': float(product_group['Quantity'].sum()),
                'revenue': float(product_group['Sale net receipts'].sum()),
                'image': 'default',
                'title': product_group['Asset Title'].unique().tolist()[0],
                'ISRC': ISRC,
            }
            artist_data['products'].append(product_data)
        artist_data['products'].sort(key=lambda x: x['view'], reverse=True)
        output['data'].append(artist_data)
    
    output['data'].sort(key=lambda x: x['artist']['view'], reverse=True)

    return JSONResponse(content=output)

@router.get("/top_music_view")
async def top_music_view():
    data = load_csv()
    # process data
    grouped_music = data.groupby('Asset ISRC')

    # Preparing the output structure
    output = {
        'data': []
    }

    # Iterating through each music group
    for music_isrc, music_group in grouped_music:
        music_data = {
            'id': str(uuid.uuid4()),  # Generating a fake UUID
            'title': music_group['Asset Title'].iloc[0],  # Assuming the title is the same for each ISRC
            'view': float(music_group['Quantity'].sum())
        }
        output['data'].append(music_data)

    # Sorting the data by view in descending order
    output['data'].sort(key=lambda x: x['view'], reverse=True)

    return JSONResponse(content=output)

@router.get("/top_music_revenue")
async def top_music_revenue():
    data = load_csv()
    # process data
    grouped_music = data.groupby('Asset ISRC')

    # Preparing the output structure
    output = {
        'data': []
    }

    # Iterating through each music group
    for music_isrc, music_group in grouped_music:
        music_data = {
            'id': str(uuid.uuid4()),  # Generating a fake UUID
            'title': music_group['Asset Title'].iloc[0],  # Assuming the title is the same for each ISRC
            'revenue': float(music_group['Sale net receipts'].sum())
        }
        output['data'].append(music_data)

    # Sorting the data by view in descending order
    output['data'].sort(key=lambda x: x['revenue'], reverse=True)

    return JSONResponse(content=output)

@router.get("/top_view_countery")
async def top_view_countery():
    data = load_csv()
    # process data
    grouped_countries = data.groupby('Territory')

    # Preparing the output structure
    output = {
        'data': []
    }

    # Iterating through each country group
    for country_name, country_group in grouped_countries:
        country = pycountry.countries.get(alpha_2=country_name)
        country_data = {
            'id': str(uuid.uuid4()),  # Generating a fake UUID
            'symbol': country_name,
            'title': country.name if country else 'Unknown',
            'view': float(country_group['Quantity'].sum()),
            'revenue': float(country_group['Sale net receipts'].sum())
        }
        output['data'].append(country_data)

    # Sorting the data by view in descending order
    output['data'].sort(key=lambda x: x['view'], reverse=True)

    return JSONResponse(content=output)