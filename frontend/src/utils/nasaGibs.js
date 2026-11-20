/**
 * NASA GIBS (Global Imagery Browse Services) TrueColor Satellite Layer
 * Layer: MODIS_Terra_CorrectedReflectance_TrueColor
 * Resolution: Level 9 (~250m native satellite resolution)
 */
export function getNasaGibsTileUrl() {
  // 2 days ago guarantees 100% processed global composite without cloud latency
  const d = new Date(Date.now() - 2 * 86400000);
  const dateStr = d.toISOString().split('T')[0];
  return `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/${dateStr}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpeg`;
}

export const NASA_GIBS_ATTRIBUTION = 'Imagery &copy; NASA EOSDIS GIBS';
export const CARTODB_DARK_MATTER_URL = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
export const CARTODB_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>';

